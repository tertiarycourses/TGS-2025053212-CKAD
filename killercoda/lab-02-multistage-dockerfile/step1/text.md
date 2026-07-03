# Step 1: Create the Go source file

```bash
mkdir -p ~/lab02 && cd ~/lab02

cat > main.go <<'EOF'
package main
import ("fmt"; "net/http")
func main() {
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprintln(w, "hello from multi-stage build")
    })
    http.ListenAndServe(":8080", nil)
}
EOF
```

---
