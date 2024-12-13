import clickLink as cl
import threading

#same scrape and store as newsapiscrape
lock = threading.Lock()
allContent = {}
Threads = []

def scrapeAndStore (url):
    content = cl.scrapeLinks(url)
    if content!=None:
        with lock:
            allContent[url]=content
        print(content[:100])
    else:
        with lock:
            allContent[url]="none"

with open ('../corpuses/testLinks.txt',"r") as links:
        linkArr = links.readlines()
        for link in linkArr:
            try:
                if threading.active_count() <= 10:  # Limit the number of active threads to 10
                    thread = threading.Thread(target=scrapeAndStore, args=(link,))
                    Threads.append(thread)
                    thread.start()

                else:
                    threading.Event().wait(1)
            except:
                 pass
    
for thread in Threads:
    thread.join()


print('everthing alert!!!!')
with open('../corpuses/test2.txt','w', encoding='utf-8') as outp:
    for key,value in allContent.items():
        print(f'{key} {value}')
        outp.write(f'HEADER: {key}\n\n')
        outp.write(f'CONTENT: {value}\n\n')


