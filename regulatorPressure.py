#upstream regulator
upstreamPressureInitial = 5800
upstreamPressureFinal = 1600

upstreamSPE = 7/100

midstreamPressureInitial = 1300

upstreamDelta = upstreamSPE * (upstreamPressureInitial - upstreamPressureFinal)

midstreamPressureFinal = midstreamPressureInitial + upstreamDelta

midstreamDelta = midstreamPressureFinal - midstreamPressureInitial

downstreamPressureInitial = 1350
downStreamSPE = 7/100

downStreamDelta = downStreamSPE * midstreamDelta

print(downStreamDelta)

