          %== CODE FOR: ./bin/simpleAssignTest.m ==%
          entry  % program entry
          align
          addi R13, R0, topaddr  % init stack pointer register
          addi R14, R0, topaddr  % init frame pointer register
          subi R13, R13, 12  % Set stack to top
          addi R12, R0, 65
          sw 0(R13), R12
          addi R12, R0, 70
          sw 4(R13), R12
          addi R12, R0, 97
          sw 8(R13), R12
          lw R12, 0(R13)
          putc R12
          lw R12, 8(R13)
          putc R12
          lw R12, 4(R13)
          putc R12
          lw R12, 0(R13)
          sw 4(R13), R12
          lw R12, 4(R13)
          putc R12
          hlt  % program exit
          %== END OF PROGRAM ==%
