read -p "please enter config key: " key

cat > key.txt << END_TEXT
$key
END_TEXT

nohup python3 -u manager.py run > out.log 2>&1 &
