"""
5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.
"""

from subprocess import Popen, PIPE, run
import chardet

if __name__ == "__main__":
    encodings = set()
    for resource in ('yandex.ru', 'youtube.com'):
        args = ['ping', '-c', '2', resource]
        subping = Popen(args, stdout=PIPE)

        print("\nPopen result:")
        for line in subping.stdout:
            encodings.add(chardet.detect(line)['encoding'])
            print(line.decode('utf-8'), end='')

        # alternative method with run call
        print("\nRun command result:")
        output_lines = run(args, capture_output=True).stdout

        encodings.add(chardet.detect(output_lines)['encoding'])
        print(output_lines.decode('utf-8'))

    print(f"Кодировка выходной строки: {encodings}")

    """
    Popen result:
    PING yandex.ru (5.255.255.77): 56 data bytes
    64 bytes from 5.255.255.77: icmp_seq=0 ttl=57 time=9.220 ms
    64 bytes from 5.255.255.77: icmp_seq=1 ttl=57 time=10.096 ms
    
    --- yandex.ru ping statistics ---
    2 packets transmitted, 2 packets received, 0.0% packet loss
    round-trip min/avg/max/stddev = 9.220/9.658/10.096/0.438 ms
    
    Run command result:
    PING yandex.ru (5.255.255.77): 56 data bytes
    64 bytes from 5.255.255.77: icmp_seq=0 ttl=57 time=8.898 ms
    64 bytes from 5.255.255.77: icmp_seq=1 ttl=57 time=9.845 ms
    
    --- yandex.ru ping statistics ---
    2 packets transmitted, 2 packets received, 0.0% packet loss
    round-trip min/avg/max/stddev = 8.898/9.372/9.845/0.473 ms
    
    
    Popen result:
    PING youtube.com (173.194.221.136): 56 data bytes
    64 bytes from 173.194.221.136: icmp_seq=0 ttl=45 time=19.296 ms
    64 bytes from 173.194.221.136: icmp_seq=1 ttl=45 time=19.831 ms
    
    --- youtube.com ping statistics ---
    2 packets transmitted, 2 packets received, 0.0% packet loss
    round-trip min/avg/max/stddev = 19.296/19.563/19.831/0.268 ms
    
    Run command result:
    PING youtube.com (173.194.221.136): 56 data bytes
    64 bytes from 173.194.221.136: icmp_seq=0 ttl=45 time=18.928 ms
    64 bytes from 173.194.221.136: icmp_seq=1 ttl=45 time=20.033 ms
    
    --- youtube.com ping statistics ---
    2 packets transmitted, 2 packets received, 0.0% packet loss
    round-trip min/avg/max/stddev = 18.928/19.480/20.033/0.553 ms
    
    Кодировка выходной строки: {'ascii'}
    
    Видим, что в консоли по умолчанию кодировка ASCII.
    Что важно, chardet не всегда дает 100% точность, 
      в случае с ASCII может быть, а с юникодом будет
      вероятностная оценка < 1.
    """
