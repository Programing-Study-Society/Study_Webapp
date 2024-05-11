(async () => {
    // TODOのIDを取得
    const id = getId(window.location.href);
    
    // 送信ボタンを押した時の処理を設定する　
    document.querySelector(".delete-btn").addEventListener('click', async(e) =>{
        
        // 元々の動作を解除
        e.preventDefault();
        
        // サーバーに送信
        const res = await deleteData("/api/delete", { "id": id });
        // エラーの時に警告文を表示
        if (!res.ok) {
            alert("Todoの削除に失敗しました")
        }
        // 一覧の画面に戻る
        window.location.href = "/"
    });
})();