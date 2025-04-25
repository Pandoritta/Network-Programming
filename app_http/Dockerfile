#############################################################################
# STAGE 1 – build & publish
#############################################################################
FROM mcr.microsoft.com/dotnet/sdk:5.0 AS build
WORKDIR /src

# copy the project file first (leverages Docker cache)
COPY UtmShop/UtmShop.csproj ./UtmShop/
RUN dotnet restore ./UtmShop/UtmShop.csproj

# copy the rest of the source
COPY UtmShop/ ./UtmShop/

# publish to a self-contained folder (Release = smaller image)
RUN dotnet publish ./UtmShop/UtmShop.csproj \
    -c Release -o /app/publish

#############################################################################
# STAGE 2 – final runtime image
#############################################################################
FROM mcr.microsoft.com/dotnet/aspnet:5.0
WORKDIR /app
COPY --from=build /app/publish .

# The app listens on port 5000 by default; expose it
ENV ASPNETCORE_URLS=http://+:5000 \
    DOTNET_EnableDiagnostics=0
#  If you don’t care about HTTPS, you can delete
#  the 5001 lines everywhere—they’re optional.
EXPOSE 5000 

ENTRYPOINT ["dotnet", "UtmShop.dll"]
