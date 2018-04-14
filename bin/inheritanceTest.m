          %== CODE FOR: ./bin/inheritanceTest.m ==%
f1        sw 0(R14), R15
          addi R12, R0, 32
          putc R12
          addi R12, R0, 65
          putc R12
          addi R12, R0, 65
          putc R12
          addi R12, R0, 65
          putc R12
          addi R12, R0, 65
          putc R12
          addi R12, R0, 65
          putc R12
          addi R12, R0, 32
          putc R12
          lw R15, 0(R14)
          jr R15
          entry  % program entry
          align
          addi R14, R0, topaddr  % init stack pointer register
          addi R15, R0, topaddr  % init frame pointer register
          subi R14, R14, 12  % Set stack to top
          getc R12
          sw 0(R14), R12
          getc R12
          sw 4(R14), R12
          lw R12, 4(R14)
          putc R12
          lw R12, 0(R14)
          putc R12
          addi R14, R14, -8
          jl R15, f1
          addi R14, R14, 8
          lw R12, -4(R14)
          sw 8(R14), R12
          lw R12, 8(R14)
          putc R12
          hlt  % program exit
          %== END OF PROGRAM ==%
