# -*- coding: utf-8 -*-
import urllib2
import codecs
from sgmllib import SGMLParser
from time import sleep
import time

content = urllib2.urlopen('http://bbs.tianya.cn/post-funinfo-1317554-1.shtml').read()

f = codecs.open("./4.txt", 'w+', 'utf8')
f.write(content.decode('utf8'))
f.close()


def get_page(text):
    if text == "":
        return "0"
    pos_end = text.rindex(".")
    if pos_end == -1:
        return "0"
    pos_begin = text.rindex("-")
    if pos_begin == -1:
        return "0"
    return text[pos_begin + 1: pos_end]


class ListName(SGMLParser):
    def __init__(self):
        SGMLParser.__init__(self)
        self.is_div = ""
        self.name = []
        self.page = ""

    def start_div(self, attrs):
        for v in attrs:
            if v[1] == "bbs-content":
                self.is_div = 1
                break
            if v[1] == "bbs-content clearfix":
                self.is_div = 1
                break

    def end_div(self):
        self.is_div = ""

    def start_a(self, attrs):
        for v in attrs:
            if v[0] == "uname":
                self.name.append("作者:" + v[1])
                break

    def start_link(self, attrs):
        for v in attrs:
            if v[0] == "rel" and v[1] == "next":
                for x in attrs:
                    if x[0] == "href":
                        self.page = x[1]
                        break
                break

    def handle_data(self, text):
        if self.is_div == 1:
            self.name.append(text)

    def get_page(self):
        if self.page == "":
            return "0"
        return get_page(self.page)


f = codecs.open("./818.txt", 'w+', 'utf8')
url = 'http://bbs.tianya.cn/post-funinfo-1317554-1.shtml'
print "start get"
print "\tstart get page1 " + url
page = "1"

TIME_FORMAT = "%Y-%m-%d %X"
begin = time.strftime(TIME_FORMAT, time.localtime(time.time()))
while url != "":
    print "\tstart get page" + page + " " + url
    try:
        content = urllib2.urlopen(url).read()
    except IOError, e:
        print "open url failed:" + url, e
        print "will try 10 senconds"
        sleep(10)
        continue
    listname = ListName()
    listname.feed(content)
    if listname.page != "":
        url = listname.page
        page = listname.get_page()
    else:
        url = ""

    item_add = ''
    for item in listname.name:
        try:
            if item.find("作者") != -1:
                if 'mk' in item_add:
                    print item_add
                elif 'mark' in item_add:
                    print item_add
                elif '马克' in item_add:
                    print item_add
                elif 'mm' in item_add:
                    print item_add
                elif '顶' in item_add:
                    print item_add
                elif '记号' in item_add:
                    print item_add
                elif 'M' in item_add:
                    print item_add
                elif '留名' in item_add:
                    print item_add
                else:
                    f.write(item_add.decode('utf8').replace('\r', '').replace('\n', '').replace('\t', '') + "\r\n\n")
                item_add = ''
                item_add = item_add + item
            else:
                item_add = item_add + item
        except IOError, e:
            print item
            print e
    print "\tget finish"
    sleep(1)
f.close()
end = time.strftime(TIME_FORMAT, time.localtime(time.time()))
print "get completed"
print "start:" + begin
print "finish:" + end
