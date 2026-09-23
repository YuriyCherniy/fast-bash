run() {
    echo
    echo "Выполнена команда:"
    echo "$@"
    echo
    echo "Результат:"
    "$@"
    echo
}
