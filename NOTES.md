## VM implementation: memory segments

- ```pop local i    => addr = LCL + i; SP--; *addr = *sp```
- ```push local i   => addr = LCL +i; *SP=*addr; SP++```