# -*- coding: utf-8 -*-
import os
import json
import subprocess
import sys
import tempfile
import urllib
from bs4 import BeautifulSoup


class ApkDownLoad:
    def __init__(self, downloadDir, tempDir):
        self.downloadDir = downloadDir
        self.tempDir = tempDir

    # ----------  Linux  ----------
    # 下载fun
    def runProcess(self, commandString):
        p = subprocess.Popen(commandString, shell=True, stderr=subprocess.PIPE)
        output, err = p.communicate()

    # ----------  Linux  ----------

    # 下载连接网页
    def urlFetch(self, targetFile, targetUrl):
        # ----------  Linux  ----------
        # self.runProcess("wget --output-document \"" + targetFile + "\" \""+targetUrl+"\"")
        # ----------  Linux  ----------

        # ----------  Windows  ----------
        urllib.urlretrieve(targetUrl, targetFile)
        # ----------  Windows  ----------

    # 获取apk下载链接
    def getAllAppLinks(self, targetFileName):
        targetAppLinkList = list()
        targetData = None
        with open(self.tempDir + '/' + targetFileName, "r") as myfile:
            targetData = myfile.read()
        if targetData:
            parsed_html = BeautifulSoup(targetData, "html.parser")
            for childApp in parsed_html.find_all("li", {"class": "card"}):
                appName = childApp.find('div', {'class': 'app-desc'}).find('a').get_text()
                urlLink = childApp.find('div', {'class': 'app-desc'}).find('a').get("href")
                size = childApp.find('div', {'class': 'meta'}).find_all('span')[2].get_text()
                if str(size)[-2:] == 'MB' and float(size[:-2]) < 10:
                    targetAppLinkList.append(urlLink)
                else:
                    continue
                    # print appName, urlLink

        return targetAppLinkList

    def getAppDownloadLinks(self, targetAppLinkList):
        targetAppDownloadDict = {}
        targetData = None
        targetFileName = self.tempDir + '/' + "dummyApp.html"
        for tempUrl in targetAppLinkList:
            self.urlFetch(targetFileName, tempUrl)
            with open(targetFileName, "r") as myfile:
                targetData = myfile.read()
            if targetData:
                parsed_html = BeautifulSoup(targetData, "html.parser")
                for childApp in parsed_html.find_all("div", {"class": "qr-info"}):
                    appName = childApp.find('a').get('download')
                    urlLink = childApp.find('a').get('href')
                    print appName + '\t' + urlLink
                    targetAppDownloadDict[appName] = urlLink
        return targetAppDownloadDict

    def getAppDownloadPage(self, targetFileName):

        targetData = None
        with open(self.tempDir + '/' + targetFileName, "r") as myfile:
            targetData = myfile.read()
        if targetData:
            parsed_html = BeautifulSoup(targetData, "html.parser")
            pages = parsed_html.find_all("a", {"class": "page-item"})
            return int(pages[-2].get_text())
            # return pages

    def downloadApps(self, targetAppDownloadDict):
        for appName in targetAppDownloadDict.keys():
            targetFile = self.downloadDir + "/" + appName
            if not os.path.exists(targetFile):
                # print "Downloading:"+ appName +" to "+targetFile
                self.urlFetch(targetFile, targetAppDownloadDict[appName])


# ----------  Linux  ----------
def runProcess(commandString):
    p = subprocess.Popen(commandString, shell=True, stderr=subprocess.PIPE)
    output, err = p.communicate()


# ----------  Linux  ----------

def urlFetch(targetFile, targetUrl):
    # ----------  Linux  ----------
    # runProcess("wget --output-document \"" + targetFile + "\" \""+targetUrl+"\"")
    # ----------  Linux  ----------

    # ----------  Windows  ----------
    urllib.urlretrieve(targetUrl, targetFile)
    # ----------  Windows  ----------


tempWorkingDir = 'tem'  # 缓存目录
downloadDir = 'down'  # 下载目录
if not os.path.exists(tempWorkingDir):
    os.makedirs(tempWorkingDir)
if not os.path.exists(downloadDir):
    os.makedirs(downloadDir)

apk = ApkDownLoad(downloadDir, tempWorkingDir)
urlFetch(tempWorkingDir + '/app.html',
         'http://www.wandoujia.com/category/game')  # 打开目录网页，分为软件('http://www.wandoujia.com/category/app')和游戏('http://www.wandoujia.com/category/game')
targetAppLinkList = list()
with open(tempWorkingDir + '/app.html', "r") as myfile:
    targetData = myfile.read()
if targetData:
    parsed_html = BeautifulSoup(targetData, "html.parser")
    count = 0
    # for childApp in parsed_html.find_all("div", { "class" : "child-cate" }):        # 找到一级分类
    parent_APP = parsed_html.find_all("div", {"class": "child-cate"})  # 找到一级分类
    for parent_count in range(0, len(parent_APP)):  # 从第i-1个类目找到第j-1个类目
        child_APP = parent_APP[parent_count].find_all('a')  # 进入二级分类
        # for each in parent_APP[parent_count].find_all('a'):                         # 进入二级分类
        for child_count in range(2, len(child_APP)):  # 从第i-1个类目找到第j-1个类目
            appName = child_APP[child_count].get_text()
            print appName
            urlLink = child_APP[child_count].get("href")
            # print (urlLink)
            try:
                apk.urlFetch(tempWorkingDir + '/tem.html', urlLink)
                nums = apk.getAppDownloadPage('tem.html')
                for i in range(1, nums):  # 依次遍历每一页
                    apk.urlFetch(tempWorkingDir + '/tem.html', urlLink + '_' + str(i))

                    apk_list = apk.getAllAppLinks('tem.html')
                    if len(apk_list) == 0:
                        continue

                    targetAppDownloadDict = apk.getAppDownloadLinks(apk_list)
                    # print targetAppDownloadDict
                    count += len(targetAppDownloadDict)
                    print count
                    apk.downloadApps(targetAppDownloadDict)

            except:
                print 'error...'
print count
