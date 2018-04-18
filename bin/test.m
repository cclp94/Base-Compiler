          %== CODE FOR: ./bin/test.m ==%
          entry  % program entry
          align
          addi R14, R0, topaddr  % init stack pointer register
          addi R15, R0, topaddr  % init frame pointer register
          subi R14, R14, 2400  % Set stack to top
          addi R12, R0, 0
          addi R11, R0, 1
          muli R11, R11, 1
          add R12, R12, R11
          addi R12, R12, 1
          muli R12, R12, 2
          addi R12, R12, 0
          addi R11, R0, 0
          addi R10, R0, 0
          muli R10, R10, 3
          add R11, R11, R10
          addi R10, R0, 2
          muli R10, R10, 1
          add R11, R11, R10
          addi R11, R11, 1
          muli R11, R11, 200
          addi R11, R11, 0
          add R11, R11, R12
          addi R12, R0, 4
          add R10, R14, R11
          sw 0(R10), R12
          addi R12, R0, 0
          addi R10, R0, 95
          muli R10, R10, 1
          add R12, R12, R10
          addi R12, R12, 1
          muli R12, R12, 2
          addi R12, R12, 0
          addi R10, R0, 0
          addi R11, R0, 1
          muli R11, R11, 3
          add R10, R10, R11
          addi R11, R0, 2
          muli R11, R11, 1
          add R10, R10, R11
          addi R10, R10, 1
          muli R10, R10, 200
          addi R10, R10, 0
          add R10, R10, R12
          addi R12, R0, 5
          add R11, R14, R10
          sw 0(R11), R12
          addi R12, R0, 0
          addi R11, R0, 51
          muli R11, R11, 1
          add R12, R12, R11
          addi R12, R12, 1
          muli R12, R12, 2
          addi R12, R12, 0
          addi R11, R0, 0
          addi R10, R0, 0
          muli R10, R10, 3
          add R11, R11, R10
          addi R10, R0, 0
          muli R10, R10, 1
          add R11, R11, R10
          addi R11, R11, 1
          muli R11, R11, 200
          addi R11, R11, 0
          add R11, R11, R12
          addi R12, R0, 1222
          add R10, R14, R11
          sw 0(R10), R12
          addi R12, R0, 0
          addi R10, R0, 1
          muli R10, R10, 1
          add R12, R12, R10
          addi R12, R12, 1
          muli R12, R12, 2
          addi R12, R12, 0
          addi R10, R0, 0
          addi R11, R0, 0
          muli R11, R11, 3
          add R10, R10, R11
          addi R11, R0, 2
          muli R11, R11, 1
          add R10, R10, R11
          addi R10, R10, 1
          muli R10, R10, 200
          addi R10, R10, 0
          add R10, R10, R12
          add R1, R14, R10
          lw R1, 0(R1)
          jl R15, putint
          addi R1, R0, 10
          putc R1  % Jump Line
          addi R10, R0, 0
          addi R12, R0, 95
          muli R12, R12, 1
          add R10, R10, R12
          addi R10, R10, 1
          muli R10, R10, 2
          addi R10, R10, 0
          addi R12, R0, 0
          addi R11, R0, 1
          muli R11, R11, 3
          add R12, R12, R11
          addi R11, R0, 2
          muli R11, R11, 1
          add R12, R12, R11
          addi R12, R12, 1
          muli R12, R12, 200
          addi R12, R12, 0
          add R12, R12, R10
          add R1, R14, R12
          lw R1, 0(R1)
          jl R15, putint
          addi R1, R0, 10
          putc R1  % Jump Line
          addi R12, R0, 0
          addi R10, R0, 51
          muli R10, R10, 1
          add R12, R12, R10
          addi R12, R12, 1
          muli R12, R12, 2
          addi R12, R12, 0
          addi R10, R0, 0
          addi R11, R0, 0
          muli R11, R11, 3
          add R10, R10, R11
          addi R11, R0, 0
          muli R11, R11, 1
          add R10, R10, R11
          addi R10, R10, 1
          muli R10, R10, 200
          addi R10, R10, 0
          add R10, R10, R12
          add R1, R14, R10
          lw R1, 0(R1)
          jl R15, putint
          addi R1, R0, 10
          putc R1  % Jump Line
          hlt  % program exit
          %== END OF PROGRAM ==%
buf       res 20  % mem for moon lib subroutines
