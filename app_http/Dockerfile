# Dockerfile for the UtmShop app
# STAGE 1 – build & publish

FROM mcr.microsoft.com/dotnet/sdk:5.0 AS build
WORKDIR /src

COPY UtmShop/UtmShop.csproj ./UtmShop/
RUN dotnet restore ./UtmShop/UtmShop.csproj


COPY UtmShop/ ./UtmShop/


RUN dotnet publish ./UtmShop/UtmShop.csproj \
    -c Release -o /app/publish

# STAGE 2 – final runtime image

FROM mcr.microsoft.com/dotnet/aspnet:5.0
WORKDIR /app
COPY --from=build /app/publish .


ENV ASPNETCORE_URLS=http://+:5000 \
    DOTNET_EnableDiagnostics=0

EXPOSE 5000 

ENTRYPOINT ["dotnet", "UtmShop.dll"]
