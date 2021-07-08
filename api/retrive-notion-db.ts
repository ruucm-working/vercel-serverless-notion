import { allowCors } from "./../utils"
import { NowRequest, NowResponse } from "@vercel/node"
import { Client } from "@notionhq/client"

const handler = async (req: NowRequest, res: NowResponse) => {
  const { query }: any = req
  console.log("query", query)
  const { id, NOTION_KEY, NOTION_DATABASE_ID } = query

  try {
    const notion = new Client({ auth: NOTION_KEY })

    const myPage = await notion.databases.query({
      database_id: NOTION_DATABASE_ID,
      // filter: {
      //   or: [
      //     {
      //       property: "Status",
      //       select: {
      //         equals: "Reading",
      //       },
      //     },
      //     {
      //       property: "Publisher",
      //       select: {
      //         equals: "NYT",
      //       },
      //     },
      //   ],
      // },
    })

    console.log("myPage!", myPage)
    console.log("myPage.results[0].properties", myPage.results[0].properties)

    res.json({ myPage })
  } catch (error) {
    console.error(error)
  }
}

export default allowCors(handler)
