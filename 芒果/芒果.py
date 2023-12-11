'''
curl 'https://pcvideohwyunott.titan.mgtv.com/c1/2023/11/02_0/8F3B2BA1368A4CAB25AD0597F8679929_20231102_1_1_932_mp4/8E9F1DE80C1E4D4C7232FCF9E7E06FD1.m3u8?arange=0&pm=0vWn4xx4BkAMcRIiQYAd1wNBvmgH8CVVE9eo7SMSsZXuSed7K1zX2FJsok09B~HoraLRLNYCxM836lajMwSFAl4DIJjPrJPtdVvPLMk8OYG~9ef5k1dIdupGI7LB5TVbQMiYvRFrDZYHCBoC5CBtwq6EDjMBuWTAa0wBOBg~FuYLZrhjnzLMvcphvdaYqzx~mty~gkStYhIWZmg7Bk0tPTkcX1FZH6btthBNNz5GkYeyitkO8Zzcu7RGV91v6wUXLsu1mtc_U7wz3BZvBD9zNigQ8Yfv3Yqe9RJoOgs4CyvfQznGOYhEsRjIqbarvWIst6pbuVYRxPSoz0uFd9blhGhIW60G9fdVqIOaDAnHKJeSwTZXxEEzlfXHkTv_2OzJsHr_yC3VhBOyYtrexX7TG5oKbsBz4RRF~7Ukzvn0Tr0-&mr=jNLFqEtqNh680DkNO44JEnwNjyenPz4RJZcFtBLUA9VccaiPSGPN1RIJMpa0DIJvdRSdNgx9iCabPblun2T4nlM5NFfW~wVrxkupCB0m3xgW2cImltD1e~Zb20KvyPfT2Xnr0bqjfl849n9LSvUDIBmsDbbRGoyBcQJG8Naz0Nlqw88V0gLK68MDVg_282JNk6CRD7EE_P0QbgqyfvANVJReqRB8VBXfdovLK1E_Hj9T0HYx8GwoVi8jvdSuqQEdDYbjTvHEmhWy4oltVPol3rqaymdYfbkAwBXjdWRHbsSxghQXdPeoRr3npqRe5nrRov1Ma36UjTW6MZ_Kb9MherzvWVwSCnFlR1BI7ZeVNiNQSh3WA0LOQ7vndF0ZZDBMvC2wtsRBJZNtClZxRRnAFtUuIQFvJtkfk39TgGx72BHjHmh7VcsQINzh0BSvbaFrxhKTUQAVGZAgHjBBXRzfMF0uKzF2jhjTK1Tk2vUqJRMlzC1WaiMKvSMyu1EZY4Z5ntI5rjtcHEiYUQNsF~a9~96fhcm3j~ZGrZSDAHQ~BLjSDa3kW~6FCzATB8glpKNk0YSui8Wjtefcc6XMDuRtBrLh3U7cbIQ8eNuvpOuY6IajYEhA8Wqjp6zqyNJVlJdmCPBiKJckwOmkHfAswh0Ylw--&uid=null&scid=25065&cpno=6i06rp&ruid=cb892ee685944524&sh=1&ftc=webO1&sftc=v6.7.38ds1_vtp1' \
  -H 'Accept: */*' \
  -H 'Accept-Language: zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6' \
  -H 'Connection: keep-alive' \
  -H 'DNT: 1' \
  -H 'Origin: https://www.mgtv.com' \
  -H 'Referer: https://www.mgtv.com/' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' \
  --compressed

'''
import os

import requests

m3u8_url = 'https://pcvideomigu.titan.mgtv.com/c1/2023/06/13_0/903AA7653521CEDB3180B4F1770F308D_20230613_1_1_264_mp4/06C40A80032B2502FED66B2394309761.m3u8?arange=0&pm=2uq5gFDG1DfLjmemcePF_YfTp34Xa_~g3sPo4kXMg8ONthMau26HFZutPdVZ1Z2AMj4gnPeX00GxQRipS_0t1vaSeskfVGGNwAt_UJlko2LOy2CbYd2H3TSzQnqr9m54amav2RaOknTmUZ~pbn5ay6BX2nVoPbh3JnYxjYBpS49egZjMwdFNQH_Q12kyRMPHKO7t6x1cr03Mt5K3Pz9q8UfiV18bRlzFMcE3DSfX88VPYzgm899zBhXe0JAk1GRF9Uqlq1aJ2pF73IK5N4MivBtmkyZz0NCNnsyN_RW_EXxO5K94TWaQQeldnWdL~chF7Od85VL_4p1t_9XJ_msmbpQJMa_GQFAGo70f~pkNtpyJ89ZK2ph9xhGSVRNH63gCU1ReqT2d85hTTrPZf9NLLDYC_Q0-&mr=CrVpfNLygONAoLlROagXe9A2xELSqH4NFZtMYeJ7tDIcmDw_H0jQ_klwFxO5cLIRn8BYzKN_aMp4tw131iLGbdy~YhKmgXWtaQVyIxSmNCwoCLGXe10mbckhSLM7U0LEX1b5udC_60L6zVZ6cTc6HeqHgBXiNYft46UsZBWAajtXwaSIQ21EYIOl2qrgmHxjeqgiZgm3GTmDE345wh8yEBTfKrtx6XD0vEMbTsCUQ~0u6SYxS2N4MsXYMTNe_4Kqy1ImyQLAEVsfSjV~OJW4bYaU0lZnzZEYCz3xKM0sD8mVap8CWab5ZCkvr4Bm2MKP70uXTjw4tXsmNFSkmFmxRxXNKmctxP7hUmIKY~K~2nne6NwCz5TUcchGgpHhkRw0kYDIZIpfu8rjca66puTLAzkE1o06Bf6A4ywd_KhuBUtMS8pdb9KwdizvISAUJHMHJKs7am30Tpk~p2YREDB_R6JYSXwJb9NZi9ehJjH4Zfye42cEJetaEQMjyN1PsyDLc4USLcVkAyDh~FZktthJ4qPnNXe5~0lsMf94Km~Mf1625CoJKnLtEw31TowICkuZu0eOSZM1gjvlEIwi1Tw3xHBWW6aA~VPWEKzXNGMfG~nbWDU88CfkyVajxtfCth_yQwe3SGWCfpOt24UjC2ZLEA--&uid=null&scid=25121&cpno=6i06rp&ruid=873904a5d46649bc&sh=1&ftc=webO1&sftc=v6.7.38ds1_vtp1'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Referer': 'https://www.mgtv.com/',
    'Origin': 'https://www.mgtv.com'
}
print('请求:', m3u8_url)
r = requests.get(m3u8_url, headers=headers)
# print(r.text)

print('开始下载')
os.system('rm -rf output.mp4')
import tqdm

urls = r.text.split('\n')
bar = tqdm.tqdm(total=len(urls))
for row in urls:
    bar.update(1)
    if row.find('.ts?') > -1:
        download_ts_url = f'https://pcvideomigu.titan.mgtv.com/{row}'
        with open(f'{bar.n}.ts', 'wb+') as w:
            print(download_ts_url)
            response_ts = requests.get(download_ts_url, headers=headers)
            w.write(response_ts.content)
