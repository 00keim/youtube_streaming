# youtube_streaming

このプログラムは、特定のYouTubeチャンネルのライブ配信のURLを、メールで通知するものです。

プログラムの主な用途としては、ライブ配信のアーカイブを限定公開にするチャンネルへの適用を想定しています。

限定公開に設定されたアーカイブには、URLを知っているユーザーしかアクセスすることができません。このプログラムを利用することで、URLがわからないからアーカイブを見れない、ということがなくなるでしょう。

# 使い方

1. Googleアカウントのアプリパスワードを生成する

    以下のサイトを参考にしてください。また、生成したアプリパスワードは2で使用するので、覚えておいてください。

    [アプリ パスワードでログインする - Google アカウント ヘルプ](https://support.google.com/accounts/answer/185833?hl=ja)

1. main.pyを書き換える

    *
        line 9

        ```
        path = '/home/username/youtube_streaming/'
        ```

        を、このフォルダまでの絶対パスに書き換えます。

    *
        line 57 ~ line 59,

        ``` 
        from_address = 'from.example@gmail.com'
        password = 'password'
        to_address = 'to.example@gmail.com'
        ```

        を、それぞれ適切なものに書き換えます。

        なお、`from_address`はアプリパスワードを生成したGoogleアカウントのメールアドレスで、送信元になります。
        `password`はアプリパスワード、`to_address`は送信先のメールアドレスです。

        **アカウントパスワード（ログインに使用するもの）ではなく、アプリパスワードを使用してください。また、アプリパスワードの漏洩には注意してください。**

1. YouTube Data API v3のAPIキーを生成する

    以下のサイトを参考にしてください。

    [YouTube Data API v3 を使って YouTube 動画を検索する](https://qiita.com/koki_develop/items/4cd7de3898dae2c33f20)

1. streamer/にファイルを置く

    YouTube Data API v3のAPIキーと、任意のYouTubeチャンネルのチャンネルIDを含むファイルを作成し、streamer/に置きます。
    ファイルの書き方は、example.txtを参考にしてください。

    * 
        複数のファイルで同一のAPIキーを使用する場合、クォータの上限を超えないように注意してください。
        このプログラムが使用するSearchメソッドは、一つのAPIキーにつき、1日100回が上限です。

        例えば、このプログラムを1時間ごとに実行する場合、4個のファイルで同一のAPIキーを使用しても問題は起こりませんが、5個のファイルだとエラーが発生するはずです。

        5つ以上のYouTubeチャンネルに対してこのプログラムを適用する場合は、適当な数のAPIキーを生成して使用してください。

    *
        チャンネルIDは、以下のサイトなどで調べることができます。

        [他人のYouTubeのチャンネルIDを調べる](https://ilr.jp/tech/485/)

    *
        streamer/にはこれら以外のファイルを置かないようにしてください。example.txtも、プログラムを実行する時は削除してください。

1. 定期的にmain.pyが実行されるように設定する
    ```
    crontab -e
    ```
    ```
    0 */1 * * * /usr/bin/python3 /home/username/youtube_streaming/main.py
    ```

# 追加したい機能

* チャンネルIDを調べずとも、YouTubeチャンネルのURLで動くようにする