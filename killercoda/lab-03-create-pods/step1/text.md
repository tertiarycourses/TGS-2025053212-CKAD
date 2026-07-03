# Step 1: Set exam-speed aliases

```bash
alias k=kubectl
export do="--dry-run=client -o yaml"
echo 'alias k=kubectl' >> ~/.bashrc
echo 'export do="--dry-run=client -o yaml"' >> ~/.bashrc
```

These two lines are the first thing to run on CKAD exam day. Every step below uses them.

---
