# Comando para pedir ao Claude a correção da Home

Copie e envie o bloco abaixo para o Claude. Ele irá aplicar o patch que evita o erro **StreamlitDuplicateElementKey** na Home:

```bash
cd /workspace/contrato-regional-ia
apply_patch <<'PATCH'
*** Begin Patch
*** Update File: Home.py
@@
-# Flag para controlar renderização da sidebar
-SIDEBAR_RENDER_FLAG = "sidebar_rendered"
+# Flag para controlar renderização da sidebar (evita widgets duplicados)
+SIDEBAR_RENDER_FLAG = "sidebar_rendered"
@@
 def render_sidebar():
-    """Renderiza a barra lateral com navegação e informações"""
-    # Garante que a sidebar seja renderizada apenas uma vez por execução da página,
-    # evitando criação duplicada de widgets com a mesma chave no Streamlit.
-    if st.session_state.get(SIDEBAR_RENDER_FLAG):
-        return
-    st.session_state[SIDEBAR_RENDER_FLAG] = True
+    """Renderiza a barra lateral com navegação e informações"""
+    # Não renderiza novamente se a flag estiver ativa (previne chaves duplicadas)
+    if st.session_state.get(SIDEBAR_RENDER_FLAG):
+        return
+    st.session_state[SIDEBAR_RENDER_FLAG] = True
@@
             if fiscais_lista:
                 fiscal_selecionado = st.selectbox(
                     "Selecione o fiscal:",
                     fiscais_lista,
                     index=fiscais_lista.index(fiscal_nome) if fiscal_nome in fiscais_lista else 0,
-                    key="select_fiscal_sidebar_home",
+                    key="select_fiscal_sidebar_home",
                 )
@@
 def main():
@@
-    # Reseta flag de renderização da sidebar a cada execução
-    st.session_state[SIDEBAR_RENDER_FLAG] = False
+    # Reseta flag de renderização da sidebar a cada execução
+    st.session_state[SIDEBAR_RENDER_FLAG] = False
*** End Patch
PATCH
```

Depois peça para ele confirmar executando:

```bash
python -m compileall Home.py
```

E finalize com um commit:

```bash
git add Home.py
git commit -m "fix: evitar chaves duplicadas na sidebar da Home"
```
