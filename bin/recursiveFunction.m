          %== CODE FOR: ./bin/recursiveFunction.m ==%
f1        sw 0(R13), R14
          addi R11, R0, 1
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
          subi R13, R13, 12  % Alloc stack for temp scope
          addi R10, R0, 1
          lw R9, 20(R13)
          sub R11, R9, R10
          sw 8(R13), R11
          lw R11, 8(R13)
          sw -4(R13), R11  % Copy parameter
          addi R13, R13, -12
          jl R14, f1
          addi R13, R13, 12
          lw R9, -8(R13)
          sw 4(R13), R9
          lw R9, 4(R13)
          lw R10, 20(R13)
          mul R11, R10, R9
          sw 0(R13), R11
          lw R11, 0(R13)
          sw 16(R13), R11
          addi R13, R13, 12  % Dealloc stack for temp scope
f4        nop  % If statement end
          lw R14, 0(R13)
          jr R14
          entry  % program entry
          align
          addi R13, R0, topaddr  % init stack pointer register
          addi R14, R0, topaddr  % init frame pointer register
          subi R13, R13, 16  % Set stack to top
          addi R12, R0, 4
          sw -4(R13), R12  % Copy parameter
          addi R13, R13, -12
          jl R14, f1
          addi R13, R13, 12
          lw R11, -8(R13)
          sw 0(R13), R11
          addi R12, R0, 4
          sw -4(R13), R12  % Copy parameter
          addi R13, R13, -12
          jl R14, f1
          addi R13, R13, 12
          lw R11, -8(R13)
          sw 4(R13), R11
          addi R11, R0, 20
          lw R10, 4(R13)
          add R12, R10, R11
          sw 8(R13), R12
          lw R10, 8(R13)
          lw R11, 0(R13)
          add R12, R11, R10
          sw 12(R13), R12
          lw R12, 12(R13)
          putc R12
          hlt  % program exit
          %== END OF PROGRAM ==%
