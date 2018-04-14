          %== CODE FOR: ./bin/functionCallTest.m ==%
f1        sw 0(R13), R14
          lw R11, 12(R13)
          lw R10, 8(R13)
          add R12, R10, R11
          sw 16(R13), R12
          lw R12, 16(R13)
          sw 4(R13), R12
          lw R14, 0(R13)
          jr R14
          entry  % program entry
          align
          addi R13, R0, topaddr  % init stack pointer register
          addi R14, R0, topaddr  % init frame pointer register
          subi R13, R13, 20  % Set stack to top
          addi R12, R0, 60
          sw 0(R13), R12
          addi R12, R0, 5
          sw 4(R13), R12
          lw R12, 0(R13)
          sw -12(R13), R12  % Copy parameter
          lw R10, 4(R13)
          sw -8(R13), R10  % Copy parameter
          addi R13, R13, -20
          jl R14, f1
          addi R13, R13, 20
          lw R11, -16(R13)
          sw 12(R13), R11
          lw R10, 12(R13)
          sw 8(R13), R10
          lw R10, 8(R13)
          sw -12(R13), R10  % Copy parameter
          lw R12, 4(R13)
          sw -8(R13), R12  % Copy parameter
          addi R13, R13, -20
          jl R14, f1
          addi R13, R13, 20
          lw R11, -16(R13)
          sw 16(R13), R11
          lw R12, 16(R13)
          putc R12
          lw R12, 8(R13)
          putc R12
          hlt  % program exit
          %== END OF PROGRAM ==%
