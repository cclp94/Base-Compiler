          %== CODE FOR: ./bin/arithAssignTest.m ==%
          entry  % program entry
          align
          addi R13, R0, topaddr  % init stack pointer register
          addi R14, R0, topaddr  % init frame pointer register
          subi R13, R13, 28  % Set stack to top
          addi R12, R0, 60
          sw 0(R13), R12
          addi R12, R0, 5
          sw 4(R13), R12
          lw R11, 4(R13)
          lw R10, 4(R13)
          mul R12, R10, R11
          sw 12(R13), R12
          lw R10, 12(R13)
          lw R11, 0(R13)
          add R12, R11, R10
          sw 16(R13), R12
          lw R12, 16(R13)
          sw 8(R13), R12
          lw R11, 4(R13)
          lw R10, 0(R13)
          add R12, R10, R11
          sw 20(R13), R12
          lw R12, 20(R13)
          putc R12
          addi R10, R0, 24
          lw R11, 4(R13)
          mul R12, R11, R10
          sw 24(R13), R12
          lw R12, 24(R13)
          sw 4(R13), R12
          lw R12, 8(R13)
          putc R12
          lw R12, 4(R13)
          putc R12
          hlt  % program exit
          %== END OF PROGRAM ==%
