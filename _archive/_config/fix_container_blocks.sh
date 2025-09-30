#!/bin/bash

# Skrypt do naprawy bloków w kontenerze Payload CMS
# Uruchom z katalogu projektu: bash _config/fix_container_blocks.sh

CONTAINER_ID="f208f37ad945"
CONFIG_DIR="_config/payload"

echo "🔧 NAPRAWA BLOKÓW W KONTENERZE PAYLOAD CMS"
echo "==========================================="

# 1. Sprawdź czy kontener działa
echo "1. Sprawdzanie kontenera..."
docker ps | grep $CONTAINER_ID > /dev/null
if [ $? -ne 0 ]; then
    echo "❌ Kontener nie działa! Uruchom go najpierw."
    exit 1
fi
echo "✅ Kontener działa"

# 2. Kopiuj kolekcję Media
echo ""
echo "2. Kopiowanie kolekcji Media..."
docker cp $CONFIG_DIR/collections/Media.ts $CONTAINER_ID:/app/src/collections/Media.ts
if [ $? -eq 0 ]; then
    echo "✅ Skopiowano Media.ts"
else
    echo "❌ Błąd podczas kopiowania Media.ts"
fi

# 3. Kopiuj poprawione bloki
echo ""
echo "3. Kopiowanie poprawionych bloków..."
docker cp $CONFIG_DIR/blocks/PricingBlockFixed.ts $CONTAINER_ID:/app/src/blocks/PricingBlock.ts
if [ $? -eq 0 ]; then
    echo "✅ Skopiowano PricingBlock"
else
    echo "❌ Błąd podczas kopiowania PricingBlock"
fi

docker cp $CONFIG_DIR/blocks/MediaBlockFixed.ts $CONTAINER_ID:/app/src/blocks/MediaBlock.ts
if [ $? -eq 0 ]; then
    echo "✅ Skopiowano MediaBlock"
else
    echo "❌ Błąd podczas kopiowania MediaBlock"
fi

# 4. Kopiuj pozostałe bloki
echo ""
echo "4. Kopiowanie pozostałych bloków..."
for block in CTABlock.ts FAQBlock.ts GalleryBlock.ts TestimonialBlock.ts; do
    if [ -f "$CONFIG_DIR/blocks/$block" ]; then
        docker cp $CONFIG_DIR/blocks/$block $CONTAINER_ID:/app/src/blocks/$block
        echo "✅ Skopiowano $block"
    fi
done

# 5. Wykonaj restart w kontenerze
echo ""
echo "5. Restartowanie aplikacji..."
docker exec $CONTAINER_ID sh -c "cd /app && npm run build"

echo ""
echo "==========================================="
echo "✅ ZAKOŃCZONO NAPRAWĘ"
echo ""
echo "CO DALEJ:"
echo "1. Otwórz panel admina: http://localhost:3458/admin"
echo "2. Edytuj dowolną stronę lub usługę"
echo "3. Sprawdź czy bloki działają poprawnie"
echo ""
echo "JEŚLI NADAL SĄ BŁĘDY:"
echo "- Sprawdź logi: docker logs -f $CONTAINER_ID"
echo "- Wyczyść cache przeglądarki (Ctrl+Shift+R)"
echo "- Zrestartuj kontener: docker restart $CONTAINER_ID"
