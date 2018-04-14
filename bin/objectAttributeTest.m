          %== CODE FOR: ./bin/objectAttributeTest.m ==%
          entry  % program entry
          align
          addi R13, R0, topaddr  % init stack pointer register
          addi R14, R0, topaddr  % init frame pointer register
          subi R13, R13, 16  % Set stack to top
          addi R12, R0, 8
          sw 4(R13), R12
          addi R12, R0, 4
          sw 8(R13), R12
          addi R11, R0, 61
          lw R10, 8(R13)
          add R12, R10, R11
          sw 12(R13), R12
          lw R12, 12(R13)
          putc R12
          hlt  % program exit
          %== END OF PROGRAM ==%
