run() {
  echo "Выполненная команда:"
  echo
  echo "$*"
  echo "==="
  echo
  eval "$*"
}