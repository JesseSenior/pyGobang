cd $PSScriptRoot/../
conda activate pyGobang_env

nuitka .\pyGobang.py `
    --onefile `
    --remove-output `
    --full-compat `
    --windows-disable-console `
    --plugin-enable=pylint-warnings `
    --plugin-enable=numpy `
    --windows-icon-from-ico=res/image/icon.ico `
    --file-reference-choice=runtime `
    --include-data-dir=res=res `
    --include-data-file=script/dllpatch/*.dll=./ `
    -o "pyGobang_Win_$env:PROCESSOR_ARCHITECTURE.exe" `

pause