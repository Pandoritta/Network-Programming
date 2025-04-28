import os
import json
import google.oauth2.credentials
import google_auth_oauthlib.flow
import google.auth.transport.requests
from google.auth.exceptions import RefreshError
import credentials as cr

class OAuthToken:
    
    def __init__(self):
        self.creds = None

    @staticmethod
    def check_secret_exists():
        if not os.path.exists(cr.CLIENT_SECRETS_FILE):
            return None

    def print_auth_url(self):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            cr.CLIENT_SECRETS_FILE, cr.SCOPES)
        flow.redirect_uri = cr.REDIRECT_URI
        authorization_url, state = flow.authorization_url(
            access_type='offline', 
            include_granted_scopes='true',
            prompt='consent')
        print(f'\nPlease visit this URL to authorize this application: {authorization_url}')
        return flow

    def client_secrets_check(self,token_data, client_secrets_file):
        if 'client_id' not in token_data or 'client_secret' not in token_data:
            with open(client_secrets_file, 'r') as f:
                all_secrets_data = json.load(f)
                secrets = all_secrets_data.get('installed') or all_secrets_data.get('web')
                if not secrets:
                    secrets = {}
                token_data['client_id'] = secrets.get('client_id')
                token_data['client_secret'] = secrets.get('client_secret')
                if not token_data['client_id'] or not token_data['client_secret']:
                    print(f"WARNING: client_id or client_secret still not found after checking {client_secrets_file}.")
        return token_data

    def save_token_to_file(self, creds, token_file, client_secrets_file):
        try:
            with open(token_file, 'w') as token_f:
                token_data = json.loads(creds.to_json())
                
                try:
                    token_data = self.client_secrets_check(token_data, client_secrets_file)
                except FileNotFoundError:
                    return False
                except json.JSONDecodeError:
                    return False
                except Exception as cs_e:
                    return False
                
                json.dump(token_data, token_f)
            return True

        except Exception as e:
            return False    

    def _run_initial_auth_flow(self):
        print("Starting new authorization flow...")
        self.check_secret_exists()

        try:
            flow = self.print_auth_url()
            auth_response = None
            while not auth_response:
                auth_response = input('\nEnter the authorization code from the callback URL/page: ').strip()
                if not auth_response:
                    print("Authorization code cannot be empty. Please try again.")
            flow.fetch_token(code=auth_response)
            creds = flow.credentials

            self.save_token_to_file(creds, cr.TOKEN_FILE, cr.CLIENT_SECRETS_FILE)
            return creds

        except Exception as e:
            return None

    def get_oauth_credentials(self):
        creds = None

        if os.path.exists(cr.TOKEN_FILE):
            try:
                creds = google.oauth2.credentials.Credentials.from_authorized_user_file(
                    cr.TOKEN_FILE, cr.SCOPES)
            except Exception as e:
                creds = None 

        if creds and not creds.valid:
            if creds.refresh_token:
                try:
                    request = google.auth.transport.requests.Request()
                    creds.refresh(request)
                    self.save_token_to_file(creds, cr.TOKEN_FILE, cr.CLIENT_SECRETS_FILE)

                except RefreshError as e:
                    return None 
                except Exception as e:
                    return None 
            else:
                return None 
            
        if not creds or not creds.valid:
            creds = self._run_initial_auth_flow() 

        if creds and creds.valid:
            return creds
        else:
            return None
        
if __name__ == "__main__":
    tokenito = OAuthToken()
    get_tokenito = tokenito.get_oauth_credentials()
    if get_tokenito:
        print("Token obtained successfully.")
    else:
        print("Failed to obtain token.")
