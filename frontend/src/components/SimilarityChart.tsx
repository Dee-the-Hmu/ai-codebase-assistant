import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts"

type CitationResponse = {
  file_path: string
  start_line: number | null
  end_line: number | null
  similarity_score: number
}

type SimilarityChartProps = {
  citations: CitationResponse[]
}

type ChartDataItem = {
  name: string
  similarity: number
  filePath: string
  lineRange: string
}

type TooltipPayload = {
  payload: ChartDataItem
}

type CustomTooltipProps = {
  active?: boolean
  payload?: TooltipPayload[]
}

function CustomTooltip({
  active,
  payload,
}: CustomTooltipProps) {
  if (!active || !payload?.length) {
    return null
  }

  const data = payload[0].payload

  return (
    <div className="max-w-sm rounded-xl border border-slate-700 bg-slate-950 p-4 shadow-2xl">
      <p className="break-all text-sm font-semibold text-slate-100">
        {data.filePath}
      </p>

      <p className="mt-1 text-xs text-slate-400">
        Lines {data.lineRange}
      </p>

      <p className="mt-3 text-sm font-medium text-violet-300">
        Similarity: {data.similarity}%
      </p>
    </div>
  )
}

export default function SimilarityChart({
  citations,
}: SimilarityChartProps) {
  const chartData: ChartDataItem[] = citations.map(
    (citation, index) => ({
      name: `Source ${index + 1}`,
      similarity: Number(
        (citation.similarity_score * 100).toFixed(1),
      ),
      filePath: citation.file_path,
      lineRange: `${citation.start_line ?? "?"}-${
        citation.end_line ?? "?"
      }`,
    }),
  )

  if (chartData.length === 0) {
    return null
  }

  return (
    <section className="rounded-2xl border border-slate-800 bg-slate-950/70 p-6 shadow-xl">
      <div className="mb-6 flex items-start justify-between gap-4">
        <div>
          <h2 className="text-xl font-semibold text-slate-100">
            Retrieval Similarity Scores
          </h2>

          <p className="mt-1 text-sm text-slate-400">
            Higher scores indicate that a source chunk is more relevant
            to the question.
          </p>
        </div>

        <div className="rounded-full border border-violet-500/30 bg-violet-500/10 px-3 py-1 text-xs font-medium text-violet-300">
          {chartData.length} chunks retrieved
        </div>
      </div>

      <div className="h-[460px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={chartData}
            layout="vertical"
            margin={{
              top: 10,
              right: 40,
              left: 10,
              bottom: 10,
            }}
          >
            <CartesianGrid
              strokeDasharray="3 3"
              horizontal={false}
              stroke="#334155"
            />

            <XAxis
              type="number"
              domain={[0, 100]}
              unit="%"
              tick={{
                fill: "#94a3b8",
                fontSize: 12,
              }}
              axisLine={{
                stroke: "#475569",
              }}
              tickLine={{
                stroke: "#475569",
              }}
            />

            <YAxis
              type="category"
              dataKey="name"
              width={90}
              tick={{
                fill: "#cbd5e1",
                fontSize: 12,
              }}
              axisLine={false}
              tickLine={false}
            />

            <Tooltip
              content={<CustomTooltip />}
              cursor={{
                fill: "rgba(139, 92, 246, 0.08)",
              }}
            />

            <Bar
              dataKey="similarity"
              fill="#8b5cf6"
              radius={[0, 8, 8, 0]}
              barSize={24}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </section>
  )
}
