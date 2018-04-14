          %== CODE FOR: ./bin/test.m ==%
          entry  % program entry
          align
          addi R13, R0, topaddr  % init stack pointer register
          addi R14, R0, topaddr  % init frame pointer register
          subi R13, R13, 8  % Set stack to top
          addi R12, R0, 1
          sw 0(R13), R12
          subi R13, R13, 4  % Alloc stack for for loop declaration scope
          addi R12, R0, 65
          sw 0(R13), R12
          addi R10, R0, 67
          lw R9, 0(R13)
          cle R11, R9, R10
          sw -4(R13), R11
          lw R11, -4(R13)
f1        bz R11, f2
          nop
          lw R10, 0(R13)
          putc R10
          addi R9, R0, 1
          lw R8, 0(R13)
          add R10, R8, R9
          sw -8(R13), R10
          lw R10, -8(R13)
          sw 0(R13), R10
          addi R8, R0, 67
          lw R9, 0(R13)
          cle R10, R9, R8
          sw -4(R13), R10
          lw R11, -4(R13)
          j f1
f2        nop  % End of loop
          addi R13, R13, 4  % Dealloc stack for temp scope
          addi R11, R0, 32
          putc R11
          addi R11, R0, 32
          putc R11
          addi R11, R0, 32
          putc R11
          addi R12, R0, 64
          lw R10, 0(R13)
          add R11, R10, R12
          sw 4(R13), R11
          lw R11, 4(R13)
          putc R11
          hlt  % program exit
          %== END OF PROGRAM ==%
