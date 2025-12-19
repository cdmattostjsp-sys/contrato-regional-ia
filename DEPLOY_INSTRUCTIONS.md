# Como publicar as últimas correções no GitHub

As mudanças mais recentes estão na branch local `work`. Siga os passos abaixo para enviar para o GitHub e liberar para o deploy:

1. **Configurar o remoto (se ainda não existir)**
   ```bash
   git remote add origin https://github.com/cdmattostjsp-sys/contrato-regional-ia.git
   git remote -v
   ```
   Confirme que `origin` aparece apontando para o repositório.

2. **Atualizar a branch principal local**
   ```bash
   git fetch origin
   git checkout main
   git merge origin/main
   ```
   (Se o repositório ainda não tem `origin/main`, pule o merge.)

3. **Levar as correções da branch `work` para `main`**
   ```bash
   git checkout work
   git rebase main
   git checkout main
   git merge work
   ```
   Resolva conflitos se existirem e confirme com `git status` que tudo está limpo.

4. **Enviar para o GitHub**
   ```bash
   git push origin main
   ```
   Caso encontre bloqueio de rede (ex.: `CONNECT tunnel failed 403`), tente novamente quando a rede permitir ou use uma conexão autorizada ao GitHub.

5. **Confirmar no GitHub**
   Acesse o repositório no navegador e verifique o commit mais recente em `main`. Depois, realize o novo deploy apontando para essa branch.

Dica: se preferir manter `work` como branch de desenvolvimento, também é possível fazer `git push origin work` e abrir um Pull Request para `main` via GitHub.
