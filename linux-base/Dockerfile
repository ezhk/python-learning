FROM ubuntu:latest
MAINTAINER Andrey Kiselev "kiselevandrew@yandex.ru"

RUN \
    apt update     && \
    apt upgrade -y && \
    apt install -y zsh git curl
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

CMD ["/bin/zsh"]