          %== CODE FOR: ./bin/fibonacciTest.m ==%
f1        sw 0(R13), R14
          addi R11, R0, 2
          lw R10, 8(R13)
          cle R12, R10, R11
          sw -4(R13), R12
          lw R12, -4(R13)
          bz R12, f3  % If Statement
f2        nop
          addi R11, R0, 1
          sw 4(R13), R11
          j f4
f3        nop
          addi R10, R0, 3
          lw R9, 8(R13)
          ceq R11, R9, R10
          sw -4(R13), R11
          lw R11, -4(R13)
          bz R11, f6  % If Statement
f5        nop
          addi R10, R0, 2
          sw 4(R13), R10
          j f7
f6        nop
          subi R13, R13, 20  % Alloc stack for temp scope
          addi R9, R0, 2
          lw R8, 28(R13)
          sub R10, R8, R9
          sw 8(R13), R10
          lw R10, 8(R13)
          sw -4(R13), R10  % Copy parameter
          addi R13, R13, -12
          jl R14, f1
          addi R13, R13, 12
          lw R8, -8(R13)
          sw 4(R13), R8
          addi R8, R0, 1
          lw R9, 28(R13)
          sub R10, R9, R8
          sw 16(R13), R10
          lw R10, 16(R13)
          sw -4(R13), R10  % Copy parameter
          addi R13, R13, -12
          jl R14, f1
          addi R13, R13, 12
          lw R9, -8(R13)
          sw 12(R13), R9
          lw R9, 4(R13)
          lw R8, 12(R13)
          add R10, R8, R9
          sw 0(R13), R10
          lw R10, 0(R13)
          sw 24(R13), R10
          addi R13, R13, 20  % Dealloc stack for temp scope
f7        nop  % If statement end
f4        nop  % If statement end
          lw R14, 0(R13)
          jr R14
          entry  % program entry
          align
          addi R13, R0, topaddr  % init stack pointer register
          addi R14, R0, topaddr  % init frame pointer register
          subi R13, R13, 8  % Set stack to top
          addi R12, R0, 10
          sw -4(R13), R12  % Copy parameter
          addi R13, R13, -12
          jl R14, f1
          addi R13, R13, 12
          lw R11, -8(R13)
          sw 0(R13), R11
          addi R11, R0, 10
          lw R10, 0(R13)
          add R12, R10, R11
          sw 4(R13), R12
          lw R12, 4(R13)
          putc R12
          hlt  % program exit
          %== END OF PROGRAM ==%
