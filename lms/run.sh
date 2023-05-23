trap "killall daphne" EXIT
source ../env/bin/activate
daphne lms.asgi:application -b 0.0.0.0 -p 8001
