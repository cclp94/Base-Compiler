          %== CODE FOR: ./bin/objectClassAttributeTest.m ==%
          entry  % program entry
          align
          addi R14, R0, topaddr  % init stack pointer register
          addi R15, R0, topaddr  % init frame pointer register
          subi R14, R14, 8  % Set stack to top
          addi R12, R0, 65
          sw 4(R14), R12
          lw R12, 4(R14)
          putc R12
          hlt  % program exit
          %== END OF PROGRAM ==%
