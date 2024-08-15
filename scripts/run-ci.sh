#!/bin/bash

# function to print colored text
print_color_text() {
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    case $1 in
    fail)
        echo -e "$timestamp \033[31m[  FAILURE  ]\033[0m $2"
        ;;
    ok)
        echo -e "$timestamp \033[32m[  SUCCESS  ]\033[0m $2"
        ;;
    warn)
        echo -e "$timestamp \033[33m[  WARNING  ]\033[0m $2"
        ;;
    info)
        echo -e "$timestamp \033[34m[INFORMATION]\033[0m $2"
        ;;
    *)
        echo -e "$timestamp [  NOTICE  ] $2"
        ;;
    esac
}
echo "========================================================================================="
print_color_text "info" "Welcome to ECI's Continuous Integration Test Suite."
echo "========================================================================================="
run_source_code_tests() {
    cd ./src || exit 1
    if pytest -v --cov --doctest-modules ./tests ./ >out.source_tests 2>&1; then
        print_color_text "ok" "All source code tests have passed."
    else
        print_color_text "fail" "At least one source code test has failed."
        exit 1
    fi
    cd ..
    touch out.source_test_success
}
echo "------------------------------------------------------------------------"
print_color_text "info" "Running the source code tests."
run_source_code_tests &
sleep 1
echo "------------------------------------------------------------------------"
wait
cat ./src/out.source_tests
rm ./src/out.source_tests
if [ ! -f out.source_test_success ]; then
    echo "------------------------------------------------------------------------"
    print_color_text "fail" "One or more tests have failed. Exiting..."
    echo "------------------------------------------------------------------------"
    exit 1
else
    echo "------------------------------------------------------------------------"
    print_color_text "ok" "All tests have passed! You are good to go!"
    echo "------------------------------------------------------------------------"
    rm -f out.source_test_success
    exit 0
fi
