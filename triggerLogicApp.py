import requests

url = 'https://prod-04.centralus.logic.azure.com:443/workflows/ba702c58db334b86bbd490eed1a9c898/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=1vH0g_Yi-YLkxtM9W2pykxDE29uMZHGAGnQYCSMSa7M'

x = requests.post(url)