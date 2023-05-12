compdef _bone-bonecommand-comp bone-bonecommand

_bone-command-fzf-list-generator() {
  local header host_list

  if [ -n "$1" ]; then
    host_list="$1"
  else
    host_list=$(_ssh-host-list)
  fi

  header="
Alias|->|Command|Desc
─────|──|───────|────
"

  host_list="${header}\n${host_list}"

  echo $host_list | bonecommand column -t -s '|'
}

_bone-command-comp(){
    local -a git_branches
    local results
    result="$1"
    commands=("asd" "dasd")

    result=$(_bone-bonecommand-fzf-list-generator $result | fzf \
      --height 40% \
      --ansi \
      --border \
      --cycle \
      --info=inline \
      --header-lines=2 \
      --reverse \
      --prompt='SSH Remote > ' \
      --bind 'shift-tab:up,tab:down,bspace:backward-delete-char/eof' \
      --preview 'ssh -T -G $(cut -f 1 -d " " <<< {}) | grep -i -E "^User |^HostName |^Port |^ControlMaster |^ForwardAgent |^LocalForward |^IdentityFile |^RemoteForward |^ProxyCommand |^ProxyJump " | column -t' \
      --preview-window=right:40%
    )
    TRAPWINCH() {
      zle && { zle reset-prompt; zle -R }
    }
}

bone-command(){
  python -m bonecommand
}
