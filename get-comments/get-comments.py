import requests
import requests
import re
import time
import csv
import sys

MAX_PAGE=100000

#header={'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
#        }
header={'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
        }

top_reply_url='https://api.bilibili.com/x/v2/reply/main?jsonp=jsonp&type=1&oid={}&mode=3'
reply_url = 'https://api.bilibili.com/x/v2/reply?pn={}&type=1&oid={}&mode=3'
replies_reply_url = 'https://api.bilibili.com/x/v2/reply/reply?pn={}&type=1&oid={}&mode=3&root={}&type=1'

def get_time(ctime):
    timeArray = time.localtime(ctime)
    otherStyleTime = time.strftime("%Y.%m.%d.%H.%M.%S", timeArray)
    return str(otherStyleTime)

def get_oid(bvid):
    video_url = 'https://www.bilibili.com/video/' + bvid
    page = requests.get(video_url, headers=header).text
    aid = re.search(r'"aid":[0-9]+', page).group()[6:]
    return aid



def save_comments(Bvid):
    fname = Bvid + '_评论.csv'
    oid = get_oid(Bvid)
    with open(fname, 'w+', newline='', encoding='utf_8_sig') as f:
        csv_writer=csv.writer(f)
        page=1
        # url = reply_url.format(page, oid)
        # try:
        #     html = requests.get(url, headers=header)
        #     data = html.json()
        #     if data['data']['top_replies']:
        #         for i in data['data']['top_replies']:
        #                 if i['replies']:
        #                     for j in i['replies']:
        #                         csv_writer.writerow([j['rpid'],get_time(j['ctime']),j['member']['mid'],j['member']['uname'],j['content']['message'],url])
        #                 csv_writer.writerow([i['rpid'],get_time(i['ctime']),i['member']['mid'],i['member']['uname'],i['content']['message'],url])
        # except Exception as err:
        #     print("Error")
        #     print(url)
        #     print(err)
        #     sys.exit()
        trurl=top_reply_url.format(oid)
        trhtml = requests.get(trurl, headers=header)
        trdata = trhtml.json()
        if trdata['data']['top_replies']:
            for tri in trdata['data']['top_replies']:
                csv_writer.writerow([tri['rpid'],get_time(tri['ctime']),tri['member']['mid'],tri['member']['uname'],tri['content']['message'],trurl])
                for trrpage in range(1, MAX_PAGE):
                    trrurl=replies_reply_url.format(trrpage,oid,tri['rpid'])
                    try:
                        trrhtml = requests.get(trrurl, headers=header)
                        trrdata = trrhtml.json()
                        if trrdata['data']['replies']:
                            for trrx in trrdata['data']['replies']:
                                csv_writer.writerow([trrx['rpid'],get_time(trrx['ctime']),trrx['member']['mid'],trrx['member']['uname'],trrx['content']['message'],trrurl])
                        else:
                            break
                    except Exception as err:
                        print("Error")
                        print(trrurl)
                        print(err)
                        sys.exit()

        for page in range(1, MAX_PAGE):   # 页码这里就简单处理了
            rurl = reply_url.format(page, oid)
            print(rurl)
            try:
                rhtml = requests.get(rurl, headers=header)
                rdata = rhtml.json()
                if rdata['data']['replies']:
                    for i in rdata['data']['replies']:
                        csv_writer.writerow([i['rpid'],get_time(i['ctime']),i['member']['mid'],i['member']['uname'],i['content']['message'],rurl])
                        for rrpage in range(1, MAX_PAGE):
                            rrurl=replies_reply_url.format(rrpage,oid,i['rpid'])
                            #print(url)
                            try:
                                rrhtml = requests.get(rrurl,headers=header)
                                rrdata = rrhtml.json()
                                if rrdata['data']['replies']:
                                    for x in rrdata['data']['replies']:
                                        csv_writer.writerow([x['rpid'],get_time(x['ctime']),x['member']['mid'],x['member']['uname'],x['content']['message'],rrurl])
                                else:
                                    break
                            except Exception as err:
                                print("No reply")
                                print(rrurl)
                                print(err)
                                sys.exit()
                else:
                    break
            except Exception as err:
                print("Error")
                print(rurl) 
                print(err)
                sys.exit()
            time.sleep(5)
        
if __name__ == '__main__':
    Bvid="BV1zr4y1i7Gf"
    save_comments(Bvid)