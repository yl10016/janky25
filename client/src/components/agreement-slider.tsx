import { Slider } from "@/components/ui/slider";
import { Label } from "@/components/ui/label";

interface AgreementSliderProps {
  articleId: number;
  onChange?: (value: number) => void;
}

export default function AgreementSlider({ articleId, onChange }: AgreementSliderProps) {
  return (
    <div className="space-y-4">
      <Label className="text-lg font-semibold">
        How much do you agree with this article?
      </Label>
      <div className="px-2">
        <Slider
          defaultValue={[3]}
          max={5}
          min={1}
          step={1}
          onValueChange={(value) => onChange?.(value[0])}
        />
        <div className="flex justify-between mt-2 text-sm text-muted-foreground">
          <span>Strongly Disagree</span>
          <span>Strongly Agree</span>
        </div>
      </div>
    </div>
  );
}
