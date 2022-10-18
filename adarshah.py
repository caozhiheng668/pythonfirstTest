import urllib.request
import urllib.parse
import json
from lxml import etree

# ctrl + shift  + s   小黑窗口
def create_request(td, page):
    if page == '64-1a-1a':
        vv = page.split("-")
        page = vv[0] + "-" + vv[1]
    base_url = "https://api.adarshah.org/plugins/adarshaplugin/file_servlet/sutra/texts?page="
    std = td
    nurl = base_url + page + "&size=20&lang=bo&sutra=" + std + "&apiKey=ZTI3Njg0NTNkZDRlMTJjMWUzNGM3MmM5ZGI3ZDUxN2E%3D"
    data = {}

    data = urllib.parse.urlencode(data).encode('utf-8')

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    }

    request = urllib.request.Request(url=nurl, headers=headers, data=data)

    return request


def get_content(request):
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')
    return content


def down_load(tdName,page, content):
    with open('dbfz_' + tdName+"_"+page + '.json', 'w', encoding='utf-8')as fp:
        fp.write(content)


if __name__ == '__main__':
    # xpath解析本地文件
    tree = etree.parse('idx.html')
    # 查询id的值以l开头的li标签
    li_list = tree.xpath('//li/ul/li/@aria-labelledby')
    # 判断列表的长度
    # print(li_list)
    # print(len(li_list))
    address_List = []
    for i in li_list:
        x = i.split("_anchor")
        zuHe = x[0].split("TD")[1]
        #  print(zuHe)
        chai = zuHe.split("-")  # chai[0]=11 chai[1]=1 chai[2]=1a
        ss = chai[0] + "-" + chai[1] + "-" + "1a"
        tdLen = len(chai[0])  # 11  101  2979  72218  257758
        if tdLen == 2:
            diYi = "TD" + chai[0][0] + "," + chai[0][1] + "-" + chai[1] + "-" + "1a"
            address_List.append(diYi)
        #    print(diYi)
        elif tdLen == 3:
            diYi = "TD" + str(chai[0][0]) + str(chai[0][1]) + "," + str(chai[0][2]) + "-" + chai[1] + "-" + "1a"
            address_List.append(diYi)
        #   print(diYi)
        elif tdLen == 4 or tdLen == 5:
            if tdLen == 4:
                diYi = "TD" + str(chai[0][0]) + str(chai[0][1]) + str(chai[0][2]) + "," + str(chai[0][3]) + "-" + chai[
                    1] + "-" + "1a"
                address_List.append(diYi)
            #   print(diYi)
            else:
                diYi = "TD" + str(chai[0][0]) + str(chai[0][1]) + str(chai[0][2]) + "," + str(chai[0][3]) + str(
                    chai[0][4]) + "-" + chai[
                           1] + "-" + "1a"
                address_List.append(diYi)
            #   print(diYi)

        elif tdLen == 6:
            diYi = "TD" + str(chai[0][0]) + str(chai[0][1]) + str(chai[0][2]) + str(chai[0][3]) + "," + str(
                chai[0][4]) + str(chai[0][5]) + "-" + chai[1] + "-" + "1a"
            address_List.append(diYi)
    # print(address_List)
    # print(len(address_List))

    for ad in address_List:
        tp = ad.split(",")
        print(tp[0] + "----" + tp[1])
        aa2 = int(tp[0].split("TD")[1])
        if aa2 == 156 :
            td1 = tp[0]
        #    page = tp[1]
            page = "6-1-1b"
            # 请求对象的定制
            request = create_request(td1, page)
            # 获取网页源码
            content = get_content(request)
            # 下载第一页
            down_load(td1,page, content)

            while True:
                if len(content) > 2:
                    obj = json.loads(content)
                    lens = len(obj)
                    # 最后一个json对象
                    lastE = obj[lens - 1]
                    # 下一页的页码
                    pbName = lastE.get("pbName")
                    # 请求对象的定制
                    request = create_request(td1,pbName)
                    # 获取网页源码
                    content = get_content(request)
                    # 下载
                    down_load(td1,pbName, content)
                    if lens == 1 or lens == 2 or lens == 3:
                        break
                    print("正在下载")
                else:
                    print("先暂时结束")
                    break
