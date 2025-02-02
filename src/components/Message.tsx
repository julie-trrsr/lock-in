export function Message({
    timecode,
    content
  }: {
    timecode: string,
    content: string
  }) {
    return (
      <div className="flex flex-row">
        <p className="mr-4 text-stone-500">
          {timecode}
        </p>
        <p className="">
          {content}
        </p>
      </div>
    );
  }