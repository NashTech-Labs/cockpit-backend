{{- define "strategy" }}
{{- with .strategy }}
{{- if eq .strategy  "RollingUpdate" }}
type: RollingUpdate
rollingUpdate:
    maxSurge: {{ .rollingUpdate.maxSurge }}
    maxUnavailable: {{ .rollingUpdate.maxUnavailable }}
{{- else }}
type: Recreate
{{- end }}
{{- end }}
{{- end }}

{{- define "serviceType" }}
{{- with .Values.service }}
{{- if .type }}
{{- if  or (eq .type "NodePort") (eq .type "LoadBalancer") }}
nodePort: {{ .nodePort }}
{{- end }}
{{- end }}
{{- end }}
{{- end }}

{{- define "imagePullSecrets"}}
{{- if not ( empty .imagePullSecrets) }}
imagePullSecrets:
{{- range .imagePullSecrets}}
- name: {{ .name }}
{{- end }}
{{- end }}
{{- end }}