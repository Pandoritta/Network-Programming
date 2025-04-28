import ntplib
from datetime import datetime, timedelta, timezone

def get_ntp_time():
    client = ntplib.NTPClient()
    try:
        response = client.request('pool.ntp.org')
        return datetime.fromtimestamp(response.tx_time, tz=timezone.utc)
    except Exception as e:
        return None

def main():
    ntp_time = get_ntp_time()
    if ntp_time is None:
        return

    user_input = input("\nEnter the region in GMT format (ex: GMT+3, GMT-5): ").strip().upper()

    if not user_input.startswith("GMT") or len(user_input) < 5:
        print("Invalid format. Correct example: GMT+3")
        return

    sign = user_input[3]
    try:
        offset = int(user_input[4:])
    except ValueError:
        print("Invalid Offset.")
        return

    if not (-12 <= offset <= 14):
        print("Invalid Offset. Should be between -12 and +14.")
        return

    if sign == '+':
        adjusted_time = ntp_time + timedelta(hours=offset)
    elif sign == '-':
        adjusted_time = ntp_time - timedelta(hours=offset)
    else:
        print("Invalid Sign. Please use + or - after GMT.")
        return

    print(f"\nExact time in region {user_input} is: {adjusted_time.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()