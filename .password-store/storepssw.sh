echo "insert token for dicord"
read token
touch .password-store/discordtoken.json 
echo "{\"discord_token\":\"$token\"}" > .password-store/discord.json
echo "spotify client id"
read clientid
echo "spotify client secret"
read clientsecret
touch .password-store/spotify.json
echo "{\"client_id\":\"$clientid\",\"client_secret\":\"$clientsecret\"}" > .password-store/spotify.json