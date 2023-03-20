# bin/bash

# if file .env not exist - stop script
FILE=.env
if [ -f "$FILE" ]; then
    echo "$FILE file exists. Continue..."
else
    echo "$FILE file does not exist."
    touch $FILE
    echo "Введи токен телеграм бота"
    read token_tg
    echo "Введи id чата"
    read chat_id
    echo "TG_BOT_TOKEN=$token_tg" >> $FILE
    echo "CHAT_ID=$chat_id" >> $FILE
fi

# init venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# make start.sh
echo "Введи название сервера"
read server_name

cat venv/bin/activate > start.sh
echo "set -a" >> start.sh
echo "source $(pwd)/.env" >> start.sh
echo "set +a" >> start.sh
echo "python3 $(pwd)/monitoring.py $server_name" >> start.sh

echo $(cat start.sh)
echo "start.sh создан"


# Add crontab
crontab -l > mycron
echo "*/10 * * * * bash $(pwd)/start.sh" >> mycron
echo $(cat mycron)
crontab mycron
echo "крон добавлен"
rm mycron
