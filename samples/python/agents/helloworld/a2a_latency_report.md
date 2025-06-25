# A2A Agent Latency Test Report

**Date:** 2025-06-25 15:25:27
**Iterations per Payload:** 10

## CPU Info

```
架构：                                x86_64
CPU 运行模式：                        32-bit, 64-bit
Address sizes:                        39 bits physical, 48 bits virtual
字节序：                              Little Endian
CPU:                                  12
在线 CPU 列表：                       0-11
厂商 ID：                             GenuineIntel
型号名称：                            Intel(R) Core(TM) i7-9850H CPU @ 2.60GHz
CPU 系列：                            6
型号：                                158
每个核的线程数：                      2
每个座的核数：                        6
座：                                  1
步进：                                13
CPU(s) scaling MHz:                   92%
CPU 最大 MHz：                        4600.0000
CPU 最小 MHz：                        800.0000
BogoMIPS：                            5199.98
标记：                                fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc art arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc cpuid aperfmperf pni pclmulqdq dtes64 monitor ds_cpl vmx smx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm 3dnowprefetch cpuid_fault epb ssbd ibrs ibpb stibp ibrs_enhanced tpr_shadow flexpriority ept vpid ept_ad fsgsbase tsc_adjust sgx bmi1 avx2 smep bmi2 erms invpcid mpx rdseed adx smap clflushopt intel_pt xsaveopt xsavec xgetbv1 xsaves dtherm ida arat pln pts hwp hwp_notify hwp_act_window hwp_epp vnmi sgx_lc md_clear flush_l1d arch_capabilities
虚拟化：                              VT-x
L1d 缓存：                            192 KiB (6 instances)
L1i 缓存：                            192 KiB (6 instances)
L2 缓存：                             1.5 MiB (6 instances)
L3 缓存：                             12 MiB (1 instance)
NUMA 节点：                           1
NUMA 节点0 CPU：                      0-11
Vulnerability Gather data sampling:   Mitigation; Microcode
Vulnerability Ghostwrite:             Not affected
Vulnerability Itlb multihit:          KVM: Mitigation: VMX disabled
Vulnerability L1tf:                   Not affected
Vulnerability Mds:                    Not affected
Vulnerability Meltdown:               Not affected
Vulnerability Mmio stale data:        Mitigation; Clear CPU buffers; SMT vulnerable
Vulnerability Reg file data sampling: Not affected
Vulnerability Retbleed:               Mitigation; Enhanced IBRS
Vulnerability Spec rstack overflow:   Not affected
Vulnerability Spec store bypass:      Mitigation; Speculative Store Bypass disabled via prctl
Vulnerability Spectre v1:             Mitigation; usercopy/swapgs barriers and __user pointer sanitization
Vulnerability Spectre v2:             Mitigation; Enhanced / Automatic IBRS; IBPB conditional; PBRSB-eIBRS SW sequence; BHI SW loop, KVM SW loop
Vulnerability Srbds:                  Mitigation; Microcode
Vulnerability Tsx async abort:        Mitigation; TSX disabled
```

## Summary

| Payload Size (KB) | Mean Latency (ms) | Std Deviation (ms) |
|-------------------|-------------------|--------------------|
| 1                 |              1.82 |               0.30 |
| 4                 |              1.80 |               0.26 |
| 16                |              2.07 |               0.33 |
| 64                |              2.58 |               0.18 |

## Detailed Results

<details>
<summary><strong>1 KB Payload</strong></summary>

| Run # | Latency (ms) |
|-------|--------------|
| 1     |         1.65 |
| 2     |         1.80 |
| 3     |         1.57 |
| 4     |         1.86 |
| 5     |         2.45 |
| 6     |         2.15 |
| 7     |         1.89 |
| 8     |         1.76 |
| 9     |         1.55 |
| 10    |         1.49 |

</details>

<details>
<summary><strong>4 KB Payload</strong></summary>

| Run # | Latency (ms) |
|-------|--------------|
| 1     |         1.68 |
| 2     |         1.56 |
| 3     |         2.13 |
| 4     |         2.19 |
| 5     |         1.87 |
| 6     |         2.15 |
| 7     |         1.68 |
| 8     |         1.54 |
| 9     |         1.64 |
| 10    |         1.59 |

</details>

<details>
<summary><strong>16 KB Payload</strong></summary>

| Run # | Latency (ms) |
|-------|--------------|
| 1     |         2.02 |
| 2     |         2.73 |
| 3     |         2.12 |
| 4     |         2.27 |
| 5     |         1.71 |
| 6     |         1.81 |
| 7     |         1.76 |
| 8     |         1.83 |
| 9     |         2.03 |
| 10    |         2.43 |

</details>

<details>
<summary><strong>64 KB Payload</strong></summary>

| Run # | Latency (ms) |
|-------|--------------|
| 1     |         2.71 |
| 2     |         2.62 |
| 3     |         2.40 |
| 4     |         2.31 |
| 5     |         2.45 |
| 6     |         2.87 |
| 7     |         2.81 |
| 8     |         2.53 |
| 9     |         2.66 |
| 10    |         2.46 |

</details>

