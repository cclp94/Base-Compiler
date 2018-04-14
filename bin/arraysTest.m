          %== CODE FOR: ./bin/arraysTest.m ==%
          entry  % program entry
          align
          addi R13, R0, topaddr  % init stack pointer register
          addi R14, R0, topaddr  % init frame pointer register
          subi R13, R13, 296  % Set stack to top
          addi R12, R0, 0
          addi R11, R0, 0
          muli R11, R11, 2
          add R12, R12, R11
          addi R11, R0, 1
          muli R11, R11, 1
          add R12, R12, R11
          addi R12, R12, 1
          muli R12, R12, 4
          addi R12, R12, 252
          addi R11, R0, 3
          add R10, R13, R12
          sw 0(R10), R11
          addi R11, R0, 1
          sw 0(R13), R11
          addi R10, R0, 2
          addi R12, R0, 1
          add R11, R12, R10
          sw 268(R13), R11
          addi R11, R0, 0
          addi R12, R0, 0
          muli R12, R12, 1
          add R11, R11, R12
          addi R11, R11, 1
          muli R11, R11, 4
          addi R11, R11, 4
          lw R12, 268(R13)
          add R10, R13, R11
          sw 0(R10), R12
          addi R12, R0, 0
          addi R10, R0, 0
          muli R10, R10, 1
          add R12, R12, R10
          addi R12, R12, 1
          muli R12, R12, 4
          addi R12, R12, 4
          addi R11, R0, 2
          add R9, R13, R12
          lw R9, 0(R9)
          mul R10, R9, R11
          sw 272(R13), R10
          addi R10, R0, 0
          addi R9, R0, 1
          muli R9, R9, 1
          add R10, R10, R9
          addi R10, R10, 1
          muli R10, R10, 4
          addi R10, R10, 4
          lw R9, 272(R13)
          add R11, R13, R10
          sw 0(R11), R9
          addi R9, R0, 0
          addi R11, R0, 1
          muli R11, R11, 1
          add R9, R9, R11
          addi R9, R9, 1
          muli R9, R9, 4
          addi R9, R9, 4
          addi R10, R0, 61
          add R12, R13, R9
          lw R12, 0(R12)
          add R11, R12, R10
          sw 276(R13), R11
          lw R11, 276(R13)
          putc R11
          addi R11, R0, 0
          addi R12, R0, 0
          muli R12, R12, 20
          add R11, R11, R12
          addi R12, R0, 0
          muli R12, R12, 5
          add R11, R11, R12
          addi R12, R0, 0
          muli R12, R12, 1
          add R11, R11, R12
          addi R11, R11, 1
          muli R11, R11, 4
          addi R11, R11, 12
          addi R12, R0, 65
          add R10, R13, R11
          sw 0(R10), R12
          addi R10, R0, 0
          addi R11, R0, 0
          muli R11, R11, 2
          add R10, R10, R11
          addi R11, R0, 1
          muli R11, R11, 1
          add R10, R10, R11
          addi R10, R10, 1
          muli R10, R10, 4
          addi R10, R10, 252
          lw R9, 0(R13)
          add R8, R13, R10
          lw R8, 0(R8)
          sub R11, R8, R9
          sw 280(R13), R11
          addi R12, R0, 0
          lw R11, 280(R13)
          muli R11, R11, 20
          add R12, R12, R11
          addi R11, R0, 0
          muli R11, R11, 5
          add R12, R12, R11
          lw R11, 0(R13)
          muli R11, R11, 1
          add R12, R12, R11
          addi R12, R12, 1
          muli R12, R12, 4
          addi R12, R12, 12
          addi R11, R0, 97
          add R8, R13, R12
          sw 0(R8), R11
          addi R12, R0, 1
          lw R9, 0(R13)
          sub R8, R9, R12
          sw 288(R13), R8
          addi R11, R0, 0
          addi R8, R0, 0
          muli R8, R8, 20
          add R11, R11, R8
          lw R8, 288(R13)
          muli R8, R8, 5
          add R11, R11, R8
          addi R8, R0, 0
          muli R8, R8, 1
          add R11, R11, R8
          addi R11, R11, 1
          muli R11, R11, 4
          addi R11, R11, 12
          lw R9, 0(R13)
          add R12, R13, R11
          lw R12, 0(R12)
          add R8, R12, R9
          sw 292(R13), R8
          lw R9, 0(R13)
          addi R11, R0, 3
          add R12, R11, R9
          sw 284(R13), R12
          addi R8, R0, 0
          lw R12, 0(R13)
          muli R12, R12, 20
          add R8, R8, R12
          addi R12, R0, 3
          muli R12, R12, 5
          add R8, R8, R12
          lw R12, 284(R13)
          muli R12, R12, 1
          add R8, R8, R12
          addi R8, R8, 1
          muli R8, R8, 4
          addi R8, R8, 12
          lw R12, 292(R13)
          add R11, R13, R8
          sw 0(R11), R12
          addi R12, R0, 0
          addi R11, R0, 0
          muli R11, R11, 20
          add R12, R12, R11
          addi R11, R0, 0
          muli R11, R11, 5
          add R12, R12, R11
          addi R11, R0, 0
          muli R11, R11, 1
          add R12, R12, R11
          addi R12, R12, 1
          muli R12, R12, 4
          addi R12, R12, 12
          add R11, R13, R12
          lw R11, 0(R11)
          putc R11
          addi R11, R0, 0
          addi R12, R0, 2
          muli R12, R12, 20
          add R11, R11, R12
          addi R12, R0, 0
          muli R12, R12, 5
          add R11, R11, R12
          addi R12, R0, 1
          muli R12, R12, 1
          add R11, R11, R12
          addi R11, R11, 1
          muli R11, R11, 4
          addi R11, R11, 12
          add R12, R13, R11
          lw R12, 0(R12)
          putc R12
          addi R12, R0, 0
          addi R11, R0, 1
          muli R11, R11, 20
          add R12, R12, R11
          addi R11, R0, 3
          muli R11, R11, 5
          add R12, R12, R11
          addi R11, R0, 4
          muli R11, R11, 1
          add R12, R12, R11
          addi R12, R12, 1
          muli R12, R12, 4
          addi R12, R12, 12
          add R11, R13, R12
          lw R11, 0(R11)
          putc R11
          hlt  % program exit
          %== END OF PROGRAM ==%
