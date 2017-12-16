Sub alphabetical_testing()
    Dim ws As Worksheet
    Dim lr As Long
    Dim j As Long
    Dim rngKey As Range
    Dim rngSort As Range
    Dim ticker As String
    Dim vol As Double
    Dim writeRow As Long
    
    Set ws = ActiveSheet
    With ws
        .Range("i1").Value = "Ticker"
        .Range("l1").Value = "Total Stock Volume"
        lr = .Range("a" & Rows.Count).End(xlUp).Row
        Set rngKey = .Range("a2:a" & lr)
        Set rngSort = .Range("a1:g" & lr)
        With .Sort
            .SortFields.Clear
            .SortFields.Add rngKey
            .SetRange rngSort
            .Header = xlYes
            .MatchCase = False
            .Orientation = xlTopToBottom
            .SortMethod = xlPinYin
            .Apply
        End With
        ticker = .Range("a2").Value
        vol = .Range("g2").Value
        For j = 3 To lr + 1
         If .Range("a" & j).Value = ticker Then
                vol = vol + .Range("g" & j).Value
            ElseIf vol > 0 Then
                writeRow = .Range("i" & Rows.Count).End(xlUp).Row + 1
                .Range("i" & writeRow).Value = ticker
                .Range("l" & writeRow).Value = vol
                ticker = .Range("a" & j).Value
                vol = .Range("g" & j).Value
            Else
                ticker = .Range("a" & j).Value
                vol = .Range("g" & j).Value
            End If
        Next j
    End With
End Sub