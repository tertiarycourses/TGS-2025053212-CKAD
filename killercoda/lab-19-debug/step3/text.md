# Step 3: Diagnose: CrashLoopBackOff

```bash
k run crash --image=busybox --restart=Always -- sh -c 'echo starting; sleep 2; exit 1'
sleep 30
k get pod crash
k describe pod crash | grep -A3 "Last State"
k logs crash --previous
```

`--previous` shows what the crashed container printed before exiting. Fix the exit code in the command — in the exam, fix the container command or image per the question.

---
