"""
    main.py driver file to get transcripts from youtube videos and combined them into an excel file
"""
import time
from YoutubeAPI import *


startTime = time.time()

print("Running...")

videos = get_video_info("parsed_data_renamed_train.json")
proxy_list = [{"http": "http://50.218.57.74:80"},
              {"http": "http://50.174.145.9:80"},
              {"http": "http://50.218.57.67:80"},
              {"http": "http://50.217.22.107:80"},
              {"http": "http://50.228.141.103:80"},
              {"http": "http://50.217.22.105:80"},
              {"http": "http://50.217.22.106:80"},
              {"http": "http://50.228.83.226:80"},
              {"http": "http://50.228.141.96:80"},
              {"http": "http://50.228.141.97:80"},
              {"http": "http://50.228.141.98:80"},
              {"http": "http://50.228.141.99:80"},
              {"http": "http://50.228.141.100:80"},
              {"http": "http://50.228.141.101:80"},
              {"http": "http://50.228.141.103:80"},
              {"http": "http://50.217.153.74:80"},
              {"http": "http://50.217.153.77:80"},
              {"http": "http://50.217.153.76:80"},
              {"http": "http://50.220.21.202:80"},
              {"http": "http://50.217.153.79:80"},
              {"http": "http://50.217.153.73:80"},
              {"http": "http://50.217.153.72:80"},
              {"http": "http://50.206.111.89:80"},
              {"http": "http://50.206.111.88:80"},
              {"http": "http://50.206.111.90:80"},
              {"http": "http://50.206.111.91:80"},
              {"http": "http://50.218.57.66:80"},
              {"http": "http://50.218.57.69:80"},
              {"http": "http://50.218.57.65:80"},
              {"http": "http://50.218.57.70:80"},
              {"http": "http://50.218.57.71:80"},
              {"http": "http://50.218.57.74:80"},
              {"http": "http://50.237.89.164:80"},
              {"http": "http://50.237.89.165:80"},
              {"http": "http://50.237.89.167:80"},
              {"http": "http://50.237.89.161:80"},
              {"http": "http://50.237.89.162:80"},
              {"http": "http://50.237.89.163:80"},
              {"http": "http://50.237.89.160:80"},
              {"http": "http://50.237.89.166:80"},
              {"http": "http://50.237.89.170:80"},
              {"http": "http://50.219.7.199:80"},
              {"http": "http://50.219.7.194:80"},
              {"http": "http://50.219.7.195:80"},
              {"http": "http://50.219.7.196:80"},
              {"http": "http://50.219.7.197:80"},
              {"http": "http://50.219.7.192:80"},
              {"http": "http://50.219.7.193:80"},
              {"http": "http://50.219.7.220:80"},
              {"http": "http://50.219.7.219:80"},
              {"http": "http://50.219.7.222:80"},
              {"http": "http://50.219.7.223:80"},
              {"http": "http://50.219.7.218:80"},
              {"http": "http://50.219.7.215:80"},
              {"http": "http://50.219.7.212:80"},
              {"http": "http://50.219.7.211:80"},
              {"http": "http://50.219.7.210:80"},
              {"http": "http://50.219.7.209:80"},
              {"http": "http://50.219.7.204:80"},
              {"http": "http://50.219.7.206:80"},
              {"http": "http://50.219.7.207:80"},
              {"http": "http://50.219.7.201:80"},
              {"http": "http://50.219.7.213:80"},
              {"http": "http://50.219.7.202:80"},
              {"http": "http://50.219.7.205:80"},
              {"http": "http://50.219.7.200:80"},
              {"http": "http://50.219.7.203:80"},
              {"http": "http://50.219.7.217:80"},
              {"http": "http://50.219.7.216:80"},
              {"http": "http://50.219.7.214:80"},
              {"http": "http://50.219.7.208:80"}]

transcripts = update_transcripts_in_parallel(proxy_list, videos[500000:600000], 100)

save_as_excel(transcripts, 1000000)

endTime = time.time()
elapsedTime = endTime - startTime

minutes = (math.floor(elapsedTime / 60)) % 60
if minutes > 60:
    hours = math.floor(minutes / 60)
else:
    hours = 0
seconds = elapsedTime % 60

print(f"Program completed in %f:%2f:%2f" % (hours, minutes, seconds))
