# for ucloud
sudo apt update

# install ffmpeg
sudo apt install ffmpeg

# create env uisng venv
python3 -m venv audio_env

# activate env
source ./audio_env/bin/activate

# upgrade pip
python3 -m pip install --upgrade pip

# install requirements
python3 -m pip install -r requirements.txt