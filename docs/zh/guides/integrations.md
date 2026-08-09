# 集成到工具

除了在终端和 IDE 中使用，BugPilot 还可以集成到其他工具中。

## Zsh 插件

[zsh-bugpilot](https://github.com/l3tchupkt/zsh-bugpilot) 是一个 Zsh 插件，让你可以在 Zsh 中快速切换到 BugPilot。

**安装**

如果你使用 Oh My Zsh，可以这样安装：

```sh
git clone https://github.com/l3tchupkt/zsh-bugpilot.git \
  ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/bugpilot
```

然后在 `~/.zshrc` 中添加插件：

```sh
plugins=(... bugpilot)
```

重新加载 Zsh 配置：

```sh
source ~/.zshrc
```

**使用**

安装后，在 Zsh 中按 `Ctrl-X` 可以快速切换到 BugPilot，无需手动输入 `kimi` 命令。

::: tip 提示
如果你使用其他 Zsh 插件管理器（如 zinit、zplug 等），请参考 [zsh-bugpilot 仓库](https://github.com/l3tchupkt/zsh-bugpilot) 的 README 了解安装方法。
:::
