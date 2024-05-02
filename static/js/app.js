/* クエリパラメータで指定されたidを取得 */
const getId = (url) => {
    const Url = new URL(url);
    return Url.searchParams.get('id'); 
}


/* JSONの送信形式を整形して送信 */
// 編集する場合, 作成する場合
const postData = (url, options) => {
	return fetch(
		'http://localhost:8000' + url,
		{
            "headers": {
                "Content-Type": "application/json",
            },
            "method": "post",
		    "body": JSON.stringify(options)
		},
	)
}

// 削除する場合
const deleteData = (url, options) => {
	return fetch(
		'http://localhost:8000' + url,
		{
            "headers": {
                "Content-Type": "application/json",
            },
            "method": "delete",
		    "body": JSON.stringify(options)
		},
	)
}